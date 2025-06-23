import sqlite3
import os
from datetime import datetime, date, timedelta
import calendar

# Get the directory of the database_manager.py file itself
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(DB_DIR, 'tracku_finance.db')

def connect_db():
    return sqlite3.connect(DATABASE_NAME)

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            notes TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            notes TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists (cannot re-add).")
        return False
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")
        return False
    finally:
        conn.close()

def get_user_id(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# --- NEW FUNCTION FOR USERNAME ---
def get_username_by_id(user_id):
    """
    Retrieves the username given a user ID.
    Returns None if the user is not found.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
# --- END NEW FUNCTION ---

def add_savings_record(category, amount, notes=""):
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now()
    transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
    month = now.month
    year = now.year
    try:
        cursor.execute(
            "INSERT INTO savings (category, amount, transaction_date, month, year, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (category, amount, transaction_date, month, year, notes)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding savings record: {e}")
        return False
    finally:
        conn.close()

def add_expense_record(category, amount, notes=""):
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now()
    transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
    month = now.month
    year = now.year
    try:
        cursor.execute(
            "INSERT INTO expenses (category, amount, transaction_date, month, year, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (category, amount, transaction_date, month, year, notes)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding expense record: {e}")
        return False
    finally:
        conn.close()

def get_all_savings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date, notes FROM savings ORDER BY transaction_date DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def get_all_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT category, amount, transaction_date FROM expenses ORDER BY transaction_date DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def get_total_savings_by_month_year(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM savings WHERE month = ? AND year = ?", (month, year))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

def get_total_expenses_by_month_year(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE month = ? AND year = ?", (month, year))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

def get_expense_breakdown_by_month_year(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) AS total_amount
        FROM expenses
        WHERE month = ? AND year = ?
        GROUP BY category
        ORDER BY total_amount DESC
    ''', (month, year))
    records = cursor.fetchall()
    conn.close()
    return records

def get_savings_breakdown_by_month_year(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) AS total_amount
        FROM savings
        WHERE month = ? AND year = ?
        GROUP BY category
        ORDER BY total_amount DESC
    ''', (month, year))
    records = cursor.fetchall()
    conn.close()
    return records

def get_total_expenses_by_day_for_month_year(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    num_days = calendar.monthrange(year, month)[1]
    daily_totals = {day: 0.0 for day in range(1, num_days + 1)}
    cursor.execute(f"""
        SELECT
            CAST(strftime('%d', transaction_date) AS INTEGER) as day,
            SUM(amount)
        FROM expenses
        WHERE month = ? AND year = ?
        GROUP BY day
        ORDER BY day
    """, (month, year))
    results = cursor.fetchall()
    conn.close()
    for day, total in results:
        daily_totals[day] = total if total is not None else 0.0
    return [daily_totals[day] for day in sorted(daily_totals.keys())]

def get_total_savings_by_day_for_month_year(month, year):
    conn = connect_db()
    cursor = conn.cursor()
    num_days = calendar.monthrange(year, month)[1]
    daily_totals = {day: 0.0 for day in range(1, num_days + 1)}
    cursor.execute(f"""
        SELECT
            CAST(strftime('%d', transaction_date) AS INTEGER) as day,
            SUM(amount)
        FROM savings
        WHERE month = ? AND year = ?
        GROUP BY day
        ORDER BY day
    """, (month, year))
    results = cursor.fetchall()
    conn.close()
    for day, total in results:
        daily_totals[day] = total if total is not None else 0.0
    return [daily_totals[day] for day in sorted(daily_totals.keys())]

def get_recent_combined_transactions(limit=7):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            transaction_date,
            'Expense' as type,
            category,
            amount,
            notes
        FROM expenses
        UNION ALL
        SELECT
            transaction_date,
            'Saving' as type,
            category,
            amount,
            notes
        FROM savings
        ORDER BY transaction_date DESC
        LIMIT ?
    """, (limit,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

if __name__ == "__main__":
    print("Initializing database...")
    initialize_db()
    print("Database initialized. Tables 'users', 'savings' and 'expenses' are ready.")

    sample_username = "testuser_dashboard" # Changed for clarity in testing
    user_id = get_user_id(sample_username)
    if not user_id:
        if add_user(sample_username):
            user_id = get_user_id(sample_username)
            print(f"User '{sample_username}' added with ID: {user_id}")
        else:
            print(f"Failed to add user '{sample_username}'.")
            exit()
    else:
        print(f"User '{sample_username}' already exists with ID: {user_id}. Using existing user.")

    print(f"\nTesting get_username_by_id for ID {user_id}: {get_username_by_id(user_id)}")

    # Existing sample data additions
    add_savings_record("Future Purchase", 500.25, "Saving for new gadget")
    add_savings_record("Emergency Fund", 1000.00, "Initial emergency deposit")
    add_savings_record("General Savings", 150.75, "Small contribution")

    last_month_date_s = date.today().replace(day=1) - timedelta(days=15)
    last_month_s = last_month_date_s.month
    last_year_s = last_month_date_s.year

    conn_s = sqlite3.connect(DATABASE_NAME)
    cursor_s = conn_s.cursor()
    cursor_s.execute(
        "INSERT INTO savings (category, amount, transaction_date, month, year, notes) VALUES (?, ?, ?, ?, ?, ?)",
        ("Personal Goals", 200.00, f"{last_year_s}-{last_month_s:02d}-10 08:00:00", last_month_s, last_year_s,
         "Goal: New Laptop")
    )
    cursor_s.execute(
        "INSERT INTO savings (category, amount, transaction_date, month, year, notes) VALUES (?, ?, ?, ?, ?, ?)",
        ("General Savings", 50.00, f"{last_year_s}-{last_month_s:02d}-20 12:00:00", last_month_s, last_year_s,
         "Weekly deposit")
    )
    conn_s.commit()
    conn_s.close()
    print("Sample savings added (current and previous month).")

    print("\nAdding sample expense records:")
    add_expense_record("Food", 75.50, "Weekly shopping")
    add_expense_record("Food", 25.00, "Lunch with friends")
    add_expense_record("Food", 12.00, "Coffee")

    last_month_date_e = date.today().replace(day=1) - timedelta(days=1)
    last_month_e = last_month_date_e.month
    last_year_e = last_month_date_e.year

    conn_e = sqlite3.connect(DATABASE_NAME)
    cursor_e = conn_e.cursor()
    cursor_e.execute(
        "INSERT INTO expenses (category, amount, transaction_date, month, year, notes) VALUES (?, ?, ?, ?, ?, ?)",
        ("Travel Fare", 100.00, f"{last_year_e}-{last_month_e:02d}-15 10:00:00", last_month_e, last_year_e, "Bus fare")
    )
    cursor_e.execute(
        "INSERT INTO expenses (category, amount, transaction_date, month, year, notes) VALUES (?, ?, ?, ?, ?, ?)",
        ("School Supply", 50.00, f"{last_year_e}-{last_month_e:02d}-01 09:00:00", last_month_e, last_year_e,
         "Notebooks")
    )
    conn_e.commit()
    conn_e.close()
    print("Sample expenses added (current and previous month).")

    print("\nAll Savings Records:")
    for record in get_all_savings():
        print(record)

    print("\nAll Expense Records:")
    for record in get_all_expenses():
        print(record)

    current_month = datetime.now().month
    current_year = datetime.now().year
    print(
        f"\nTotal Savings for current month ({current_month}/{current_year}): ₱{get_total_savings_by_month_year(current_month, current_year):.2f}")
    print(
        f"Total Expenses for current month ({current_month}/{current_year}): ₱{get_total_expenses_by_month_year(current_month, current_year):.2f}")

    print(f"\nExpense Breakdown for current month ({current_month}/{current_year}):")
    for category, total in get_expense_breakdown_by_month_year(current_month, current_year):
        print(f"- {category}: ₱{total:.2f}")

    print(f"\nSavings Breakdown for current month ({current_month}/{current_year}):")
    for category, total in get_savings_breakdown_by_month_year(current_month, current_year):
        print(f"- {category}: ₱{total:.2f}")

    print(f"\nDaily Expenses for current month ({current_month}/{current_year}):")
    daily_exp = get_total_expenses_by_day_for_month_year(current_month, current_year)
    for day, amount in enumerate(daily_exp, 1):
        print(f"Day {day}: ₱{amount:.2f}")

    print(f"\nDaily Savings for current month ({current_month}/{current_year}):")
    daily_sav = get_total_savings_by_day_for_month_year(current_month, current_year)
    for day, amount in enumerate(daily_sav, 1):
        print(f"Day {day}: ₱{amount:.2f}")

    print("\nRecent Combined Transactions (Limit 5):")
    for trans in get_recent_combined_transactions(limit=5):
        print(trans)