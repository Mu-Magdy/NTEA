import sqlite3
import pandas as pd
import hashlib

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    """Create the employees table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone_number TEXT,
            department TEXT,
            position TEXT,
            hire_date TEXT,
            base_salary REAL,
            bonus REAL,
            currency TEXT,
            annual_leave_balance INTEGER,
            sick_leave_balance INTEGER,
            performance_rating REAL,
            review_period TEXT,
            last_review_date TEXT,
            password_hash TEXT,
            last_login TEXT
        )
        """
    )
    conn.commit()

def load_data_from_csv(conn, csv_file):
    """Load employee data from a CSV file into the database."""
    df = pd.read_csv(csv_file)
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, department, position,
            hire_date, base_salary, bonus, currency, annual_leave_balance, sick_leave_balance, performance_rating,
            review_period, last_review_date, password_hash, last_login)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["employee_id"],
                row["first_name"],
                row["last_name"],
                row["email"],
                row["phone_number"],
                row["department"],
                row["position"],
                row["hire_date"],
                row["base_salary"],
                row["bonus"],
                row["currency"],
                row["annual_leave_balance"],
                row["sick_leave_balance"],
                row["performance_rating"],
                row["review_period"],
                row["last_review_date"],
                row["password_hash"],
                row["last_login"],
            ),
        )
    conn.commit()

def hash_default_password(conn, default_password="password123"):
    """Hash the default password and update all employees' password hashes."""
    password_hash = hashlib.sha256(default_password.encode()).hexdigest()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        UPDATE employees
        SET password_hash = ?
        """,
        (password_hash,),
    )
    
    conn.commit()

def setup_database(csv_file):
    """Setup the employee database."""
    conn = create_connection("employee_data.db")
    create_table(conn)
    load_data_from_csv(conn, csv_file)
    hash_default_password(conn)
    conn.close()

# Uncomment the line below to run the setup
# setup_database("employees.csv")
