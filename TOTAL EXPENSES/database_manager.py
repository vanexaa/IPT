import sqlite3
import os
from datetime import datetime, date, timedelta
import calendar

# Get the directory of the database_manager.py file itself
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(DB_DIR, 'tracku_finance.db')

def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    # Enable foreign key constraints for this connection
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE
        )
    ''')

    # Modify savings table to include user_id and ON DELETE CASCADE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS savings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,  -- New column to link to users table
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    # Modify expenses table to include user_id and ON DELETE CASCADE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,  -- New column to link to users table
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
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
    Due to ON DELETE CASCADE, associated savings and expenses records will also be deleted.
    Returns True on success, False on failure.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting user with ID {user_id}: {e}")
        return False
    finally:
        conn.close()


def add_savings_record(user_id, category, amount): # Added user_id
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now()
    transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
    month = now.month
    year = now.year
    try:
        cursor.execute(
            "INSERT INTO savings (user_id, category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, category, amount, transaction_date, month, year)
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


def add_expense_record(user_id, category, amount): # Added user_id
    conn = connect_db()
    cursor = conn.cursor()
    now = datetime.now()
    transaction_date = now.strftime("%Y-%m-%d %H:%M:%S")
    month = now.month
    year = now.year
    try:
        cursor.execute(
            "INSERT INTO expenses (user_id, category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, category, amount, transaction_date, month, year)
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
    # Updated to include user_id in the select statement if needed, though not directly used here
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
    # Updated to include user_id in the select statement if needed, though not directly used here
    cursor.execute("SELECT id, category, amount, transaction_date FROM savings WHERE id = ?", (saving_id,))
    record = cursor.fetchone()
    conn.close()
    return record


def get_all_savings(user_id): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date FROM savings WHERE user_id = ? ORDER BY transaction_date DESC", (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_all_expenses(user_id): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, amount, transaction_date FROM expenses WHERE user_id = ? ORDER BY transaction_date DESC", (user_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_total_savings_by_month_year(user_id, month, year): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM savings WHERE user_id = ? AND month = ? AND year = ?", (user_id, month, year))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

def get_total_expenses_by_month_year(user_id, month, year): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = ? AND month = ? AND year = ?", (user_id, month, year))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total is not None else 0.0

def get_expense_breakdown_by_month_year(user_id, month, year): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) AS total_amount
        FROM expenses
        WHERE user_id = ? AND month = ? AND year = ?
        GROUP BY category
        ORDER BY total_amount DESC
    ''', (user_id, month, year))
    records = cursor.fetchall()
    conn.close()
    return records

def get_savings_breakdown_by_month_year(user_id, month, year): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) AS total_amount
        FROM savings
        WHERE user_id = ? AND month = ? AND year = ?
        GROUP BY category
        ORDER BY total_amount DESC
    ''', (user_id, month, year))
    records = cursor.fetchall()
    conn.close()
    return records

def get_total_expenses_by_day_for_month_year(user_id, month, year): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    num_days = calendar.monthrange(year, month)[1]
    daily_totals = {day: 0.0 for day in range(1, num_days + 1)}
    cursor.execute(f"""
        SELECT
            CAST(strftime('%d', transaction_date) AS INTEGER) as day,
            SUM(amount)
        FROM expenses
        WHERE user_id = ? AND month = ? AND year = ?
        GROUP BY day
        ORDER BY day
    """, (user_id, month, year))
    results = cursor.fetchall()
    conn.close()
    for day, total in results:
        daily_totals[day] = total if total is not None else 0.0
    return [daily_totals[day] for day in sorted(daily_totals.keys())]

def get_total_savings_by_day_for_month_year(user_id, month, year): # Filter by user_id
    conn = connect_db()
    cursor = conn.cursor()
    num_days = calendar.monthrange(year, month)[1]
    daily_totals = {day: 0.0 for day in range(1, num_days + 1)}
    cursor.execute(f"""
        SELECT
            CAST(strftime('%d', transaction_date) AS INTEGER) as day,
            SUM(amount)
        FROM savings
        WHERE user_id = ? AND month = ? AND year = ?
        GROUP BY day
        ORDER BY day
    """, (user_id, month, year))
    results = cursor.fetchall()
    conn.close()
    for day, total in results:
        daily_totals[day] = total if total is not None else 0.0
    return [daily_totals[day] for day in sorted(daily_totals.keys())]

def get_recent_combined_transactions(user_id, limit=7): # Filter by user_id
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
        WHERE user_id = ?
        UNION ALL
        SELECT
            id,
            transaction_date,
            'Saving' as type,
            category,
            amount
        FROM savings
        WHERE user_id = ?
        ORDER BY transaction_date DESC
        LIMIT ?
    """, (user_id, user_id, limit))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

if __name__ == "__main__":
    print("Initializing database...")
    initialize_db()
    print("Database initialized. Tables 'users', 'savings' and 'expenses' are ready.")

    sample_username = "testuser_dashboard"
    user_id = get_user_id(sample_username)
    if not user_id:
        if add_user(sample_username):
            user_id = get_user_id(sample_username)
            print(f"User '{sample_username}' added with ID: {user_id}")
        else:
            print(f"Failed to add user '{sample_username}'.")
    else:
        print(f"User '{sample_username}' already exists with ID: {user_id}. Using existing user.")

    print(f"\nTesting get_username_by_id for ID {user_id}: {get_username_by_id(user_id)}")

    # Existing sample data additions (ensure you add data if DB is empty or for testing purposes)
    print("\nAdding sample savings records:")
    # Now passing user_id
    add_savings_record(user_id, "Future Purchase", 500.25)
    add_savings_record(user_id, "Emergency Fund", 1000.00)
    add_savings_record(user_id, "General Savings", 150.75)

    last_month_date_s = date.today().replace(day=1) - timedelta(days=15)
    last_month_s = last_month_date_s.month
    last_year_s = last_month_date_s.year

    conn_s = connect_db() # Use the modified connect_db
    cursor_s = conn_s.cursor()
    # Check if data already exists to avoid duplicates on repeated runs
    cursor_s.execute("SELECT COUNT(*) FROM savings WHERE user_id = ? AND category = 'Personal Goals' AND month = ? AND year = ?", (user_id, last_month_s, last_year_s))
    if cursor_s.fetchone()[0] == 0:
        cursor_s.execute(
            "INSERT INTO savings (user_id, category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, "Personal Goals", 200.00, f"{last_year_s}-{last_month_s:02d}-10 08:00:00", last_month_s, last_year_s)
        )
        cursor_s.execute(
            "INSERT INTO savings (user_id, category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, "General Savings", 50.00, f"{last_year_s}-{last_month_s:02d}-20 12:00:00", last_month_s, last_year_s)
        )
        conn_s.commit()
        print("Sample savings added for last month.")
    conn_s.close()

    print("\nAdding sample expense records:")
    # Now passing user_id
    add_expense_record(user_id, "Food", 75.50)
    add_expense_record(user_id, "Food", 25.00)
    add_expense_record(user_id, "Food", 12.00)

    last_month_date_e = date.today().replace(day=1) - timedelta(days=1)
    last_month_e = last_month_date_e.month
    last_year_e = last_month_date_e.year

    conn_e = connect_db() # Use the modified connect_db
    cursor_e = conn_e.cursor()
    # Check if data already exists to avoid duplicates on repeated runs
    cursor_e.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ? AND category = 'Travel Fare' AND month = ? AND year = ?", (user_id, last_month_e, last_year_e))
    if cursor_e.fetchone()[0] == 0:
        cursor_e.execute(
            "INSERT INTO expenses (user_id, category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, "Travel Fare", 100.00, f"{last_year_e}-{last_month_e:02d}-15 10:00:00", last_month_e, last_year_e)
        )
        cursor_e.execute(
            "INSERT INTO expenses (user_id, category, amount, transaction_date, month, year) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, "School Supply", 50.00, f"{last_year_e}-{last_month_e:02d}-01 09:00:00", last_month_e, last_year_e)
        )
        conn_e.commit()
        print("Sample expenses added for last month.")
    conn_e.close()

    print("\nAll Savings Records:")
    for record in get_all_savings(user_id): # Filter by user_id
        print(record)

    print("\nAll Expense Records:")
    for record in get_all_expenses(user_id): # Filter by user_id
        print(record)

    current_month = datetime.now().month
    current_year = datetime.now().year
    print(
        f"\nTotal Savings for current month ({current_month}/{current_year}): ₱{get_total_savings_by_month_year(user_id, current_month, current_year):.2f}")
    print(
        f"Total Expenses for current month ({current_month}/{current_year}): ₱{get_total_expenses_by_month_year(user_id, current_month, current_year):.2f}")

    print(f"\nExpense Breakdown for current month ({current_month}/{current_year}):")
    for category, total in get_expense_breakdown_by_month_year(user_id, current_month, current_year): # Filter by user_id
        print(f"- {category}: ₱{total:.2f}")

    print(f"\nSavings Breakdown for current month ({current_month}/{current_year}):")
    for category, total in get_savings_breakdown_by_month_year(user_id, current_month, current_year): # Filter by user_id
        print(f"- {category}: ₱{total:.2f}")

    print(f"\nDaily Expenses for current month ({current_month}/{current_year}):")
    daily_exp = get_total_expenses_by_day_for_month_year(user_id, current_month, current_year) # Filter by user_id
    for day, amount in enumerate(daily_exp, 1):
        print(f"Day {day}: ₱{amount:.2f}")

    print(f"\nDaily Savings for current month ({current_month}/{current_year}):")
    daily_sav = get_total_savings_by_day_for_month_year(user_id, current_month, current_year) # Filter by user_id
    for day, amount in enumerate(daily_sav, 1):
        print(f"Day {day}: ₱{amount:.2f}")

    print("\nRecent Combined Transactions (Limit 5):")
    for trans in get_recent_combined_transactions(user_id, limit=5): # Filter by user_id
        print(trans)

    # --- Testing the new update functions ---
    print("\n--- Testing Update Functions ---")

    # Get a sample savings record to update
    all_savings = get_all_savings(user_id) # Filter by user_id
    if all_savings:
        first_saving = all_savings[0]
        saving_id = first_saving[0]
        print(f"Attempting to update savings record ID {saving_id}: {first_saving}")
        if update_savings_record(saving_id, "Updated Savings Category", 999.99):
            print(f"Successfully updated savings record ID {saving_id}.")
            print("Updated savings record:", get_all_savings(user_id)[0]) # Filter by user_id
        else:
            print(f"Failed to update savings record ID {saving_id}.")
    else:
        print("No savings records to update.")

    # Get a sample expense record to update
    all_expenses = get_all_expenses(user_id) # Filter by user_id
    if all_expenses:
        first_expense = all_expenses[0]
        expense_id = first_expense[0]
        print(f"Attempting to update expense record ID {expense_id}: {first_expense}")
        if update_expense_record(expense_id, "Updated Food Category", 123.45):
            print(f"Successfully updated expense record ID {expense_id}.")
            print("Updated expense record:", get_all_expenses(user_id)[0]) # Filter by user_id
        else:
            print(f"Failed to update expense record ID {expense_id}.")
    else:
        print("No expense records to update.")

    # --- Testing cascade delete ---
    print("\n--- Testing User Deletion with Cascade ---")
    another_username = "user_to_delete"
    another_user_id = get_user_id(another_username)
    if not another_user_id:
        if add_user(another_username):
            another_user_id = get_user_id(another_username)
            print(f"User '{another_username}' added with ID: {another_user_id}")
            add_savings_record(another_user_id, "Savings for Delete", 100.00)
            add_expense_record(another_user_id, "Expense for Delete", 50.00)
            print(f"Savings for {another_username}: {get_all_savings(another_user_id)}")
            print(f"Expenses for {another_username}: {get_all_expenses(another_user_id)}")

            print(f"\nDeleting user '{another_username}' (ID: {another_user_id})...")
            if delete_user(another_user_id):
                print(f"User '{another_username}' successfully deleted.")
                print(f"Checking savings for {another_username} after delete: {get_all_savings(another_user_id)}")
                print(f"Checking expenses for {another_username} after delete: {get_all_expenses(another_user_id)}")
            else:
                print(f"Failed to delete user '{another_username}'.")
        else:
            print(f"Failed to add user '{another_username}'.")
    else:
        print(f"User '{another_username}' already exists. Deleting it to re-test cascade.")
        delete_user(another_user_id)
        # Re-run the test logic if the user was already there.
        # This part of the `if __name__ == "__main__"` block could be refactored for cleaner test setup.
        # For now, we'll just indicate it was deleted.
        print(f"User '{another_username}' (ID: {another_user_id}) and associated data deleted from previous run.")