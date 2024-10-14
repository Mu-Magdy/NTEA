import sqlite3
import hashlib
import pandas as pd
import os

# Function to authenticate employee using email and password
def authenticate_employee(email, password):
    # Connect to the database
    # conn = sqlite3.connect("employee_data.db")
    database_path = os.path.abspath('../database/employee_data.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Hash the input password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Query to find the employee with matching email and password hash
    cursor.execute(
        "SELECT * FROM employees WHERE email=? AND password_hash=?",
        (email, password_hash),
    )
    employee = cursor.fetchone()
    
    query = f"SELECT * FROM employees WHERE email = '{email}' AND password_hash = '{password_hash}'"

    df = pd.read_sql(query, conn)

    conn.close()

    if employee:
        print(f"Authentication successful for: {employee[1]} {employee[2]}")
        return df.to_dict('records')
    else:
        print("Authentication failed!")
        return None
