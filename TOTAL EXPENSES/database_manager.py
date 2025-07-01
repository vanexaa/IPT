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
            year INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL
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
        print(f"User '{username}' added successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists. Please choose a different one.")
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

# NEW FUNCTION: Update username
def update_username(user_id, new_username):
    """
    Updates the username for a given user ID.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Username '{new_username}' already exists. Please choose a different one.")
        return False
    except sqlite3.Error as e:
        print(f"Error updating username for user ID {user_id}: {e}")
        return False
    finally:
        conn.close()

# NEW FUNCTION: Delete user
def delete_user(user_id):
    """
    Deletes a user from the database.
    Note: This currently only deletes the user from the 'users' table.
    If 'savings' and 'expenses' records need to be deleted with the user,
    those tables would need a 'user_id' column and corresponding DELETE CASCADE setup.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting user with ID {user_id}: {e}")
        return False
    finally:
        conn.close()


def add_savings_record(category, amount): # Removed default empty string for amount
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now()
    transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
    month = now.month
    year = now.year
    try:
        cursor.execute(
            "INSERT INTO savings (category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?)",
            (category, amount, transaction_date, month, year)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding savings record: {e}")
        return False
    finally:
        conn.close()

# NEW FUNCTION: Update Savings Record
def update_savings_record(record_id, new_category, new_amount):
    """
    Updates an existing savings record.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Get current date/time for the update
        now = datetime.now()
        transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
        month = now.month
        year = now.year

        cursor.execute(
            "UPDATE savings SET category = ?, amount = ?, transaction_date = ?, month = ?, year = ? WHERE id = ?",
            (new_category, new_amount, transaction_date, month, year, record_id)
        )
        conn.commit()
        return cursor.rowcount > 0 # Check if any row was actually updated
    except sqlite3.Error as e:
        print(f"Error updating savings record with ID {record_id}: {e}")
        return False
    finally:
        conn.close()

# NEW FUNCTION: Delete Savings Record
def delete_savings_record(record_id):
    """
    Deletes a savings record from the database.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM savings WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0 # Check if any row was actually deleted
    except sqlite3.Error as e:
        print(f"Error deleting savings record with ID {record_id}: {e}")
        return False
    finally:
        conn.close()


def add_expense_record(category, amount):
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now()
    transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
    month = now.month
    year = now.year
    try:
        cursor.execute(
            "INSERT INTO expenses (category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?)",
            (category, amount, transaction_date, month, year)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding expense record: {e}")
        return False
    finally:
        conn.close()

# NEW FUNCTION: Update Expense Record
def update_expense_record(record_id, new_category, new_amount):
    """
    Updates an existing expense record.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Get current date/time for the update
        now = datetime.now()
        transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
        month = now.month
        year = now.year

        cursor.execute(
            "UPDATE expenses SET category = ?, amount = ?, transaction_date = ?, month = ?, year = ? WHERE id = ?",
            (new_category, new_amount, transaction_date, month, year, record_id)
        )
        conn.commit()
        return cursor.rowcount > 0 # Check if any row was actually updated
    except sqlite3.Error as e:
        print(f"Error updating expense record with ID {record_id}: {e}")
        return False
    finally:
        conn.close()

# NEW FUNCTION: Delete Expense Record
def delete_expense_record(record_id):
    """
    Deletes an expense record from the database.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE id = ?", (record_id,))
        conn.commit()
        return cursor.rowcount > 0 # Check if any row was actually deleted
    except sqlite3.Error as e:
        print(f"Error deleting expense record with ID {record_id}: {e}")
        return False
    finally:
        conn.close()

# NEW FUNCTION: Get a single expense record by ID
def get_expense_by_id(expense_id):
    """
    Retrieves a single expense record by its ID.
    Returns the record as a tuple (id, category, amount, transaction_date), or None if not found.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date FROM expenses WHERE id = ?", (expense_id,))
    record = cursor.fetchone()
    conn.close()
    return record

# NEW FUNCTION: Get a single savings record by ID (for consistency)
def get_savings_by_id(saving_id):
    """
    Retrieves a single savings record by its ID.
    Returns the record as a tuple (id, category, amount, transaction_date), or None if not found.
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date FROM savings WHERE id = ?", (saving_id,))
    record = cursor.fetchone()
    conn.close()
    return record


def get_all_savings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date FROM savings ORDER BY transaction_date DESC")
    records = cursor.fetchall()
    conn.close()
    return records

def get_all_expenses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date FROM expenses ORDER BY transaction_date DESC")
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
            id,
            transaction_date,
            'Expense' as type,
            category,
            amount
        FROM expenses
        UNION ALL
        SELECT
            id,
            transaction_date,
            'Saving' as type,
            category,
            amount
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

    # Check if any user exists
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    conn.close()

    user_id = None
    if user_count == 0:
        print("\nNo users found. Let's create a new user.")
        while user_id is None:
            new_username = input("Enter a new username: ").strip()
            if new_username:
                if add_user(new_username):
                    user_id = get_user_id(new_username)
                else:
                    print("Could not create user. Please try a different username.")
            else:
                print("Username cannot be empty. Please try again.")
    else:
        print("\nExisting users found.")
        cursor = connect_db().cursor()
        cursor.execute("SELECT username FROM users")
        existing_users = [row[0] for row in cursor.fetchall()]
        connect_db().close()
        print("Available users: " + ", ".join(existing_users))

        selected_username = None
        while selected_username not in existing_users:
            selected_username = input("Enter an existing username or type 'new' to create one: ").strip()
            if selected_username.lower() == 'new':
                while user_id is None:
                    new_username = input("Enter a new username: ").strip()
                    if new_username:
                        if add_user(new_username):
                            user_id = get_user_id(new_username)
                        else:
                            print("Could not create user. Please try a different username.")
                    else:
                        print("Username cannot be empty. Please try again.")
                break # Exit the loop after creating a new user
            elif selected_username in existing_users:
                user_id = get_user_id(selected_username)
                break
            else:
                print("Username not found. Please try again or type 'new'.")

    if user_id:
        print(f"\nCurrently active user: {get_username_by_id(user_id)} (ID: {user_id})")

        print(f"\nTesting get_username_by_id for ID {user_id}: {get_username_by_id(user_id)}")

        # Existing sample data additions (ensure you add data if DB is empty or for testing purposes)
        print("\nAdding sample savings records:")
        add_savings_record("Future Purchase", 500.25)
        add_savings_record("Emergency Fund", 1000.00)
        add_savings_record("General Savings", 150.75)

        last_month_date_s = date.today().replace(day=1) - timedelta(days=15)
        last_month_s = last_month_date_s.month
        last_year_s = last_month_date_s.year

        conn_s = sqlite3.connect(DATABASE_NAME)
        cursor_s = conn_s.cursor()
        # Check if data already exists to avoid duplicates on repeated runs
        cursor_s.execute("SELECT COUNT(*) FROM savings WHERE category = 'Personal Goals' AND month = ? AND year = ?", (last_month_s, last_year_s))
        if cursor_s.fetchone()[0] == 0:
            cursor_s.execute(
                "INSERT INTO savings (category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?)",
                ("Personal Goals", 200.00, f"{last_year_s}-{last_month_s:02d}-10 08:00:00", last_month_s, last_year_s)
            )
            cursor_s.execute(
                "INSERT INTO savings (category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?)",
                ("General Savings", 50.00, f"{last_year_s}-{last_month_s:02d}-20 12:00:00", last_month_s, last_year_s)
            )
            conn_s.commit()
            print("Sample savings added for last month.")
        conn_s.close()

        print("\nAdding sample expense records:")
        add_expense_record("Food", 75.50)
        add_expense_record("Food", 25.00)
        add_expense_record("Food", 12.00)

        last_month_date_e = date.today().replace(day=1) - timedelta(days=1)
        last_month_e = last_month_date_e.month
        last_year_e = last_month_date_e.year

        conn_e = sqlite3.connect(DATABASE_NAME)
        cursor_e = conn_e.cursor()
        # Check if data already exists to avoid duplicates on repeated runs
        cursor_e.execute("SELECT COUNT(*) FROM expenses WHERE category = 'Travel Fare' AND month = ? AND year = ?", (last_month_e, last_year_e))
        if cursor_e.fetchone()[0] == 0:
            cursor_e.execute(
                "INSERT INTO expenses (category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?)",
                ("Travel Fare", 100.00, f"{last_year_e}-{last_month_e:02d}-15 10:00:00", last_month_e, last_year_e)
            )
            cursor_e.execute(
                "INSERT INTO expenses (category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?)",
                ("School Supply", 50.00, f"{last_year_e}-{last_month_e:02d}-01 09:00:00", last_month_e, last_year_e)
            )
            conn_e.commit()
            print("Sample expenses added for last month.")
        conn_e.close()

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

        # --- Testing the new update functions ---
        print("\n--- Testing Update Functions ---")
    else:
        print("\nNo user was selected or created. Exiting.")