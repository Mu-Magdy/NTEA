import sqlite3
import pandas as pd
import hashlib
import unittest
import os

class TestEmployeeDatabase(unittest.TestCase):

    def setUp(self):
        """Set up a test database and create the table."""
        self.db_name = "test_employee_data.db"
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def tearDown(self):
        """Close the database connection and remove the test database."""
        self.conn.close()
        os.remove(self.db_name)

    def create_table(self):
        """Create the employees table if it doesn't exist."""
        cursor = self.conn.cursor()
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
        self.conn.commit()

    def test_table_creation(self):
        """Test if the employees table is created successfully."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';")
        table_exists = cursor.fetchone() is not None
        self.assertTrue(table_exists, "The employees table was not created.")

    def test_data_insertion(self):
        """Test if data is inserted into the database correctly."""
        # Sample data
        sample_data = {
            "employee_id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "123-456-7890",
            "department": "Engineering",
            "position": "Software Engineer",
            "hire_date": "2022-01-01",
            "base_salary": 70000,
            "bonus": 5000,
            "currency": "USD",
            "annual_leave_balance": 15,
            "sick_leave_balance": 10,
            "performance_rating": 4.5,
            "review_period": "Annual",
            "last_review_date": "2023-01-01",
            "password_hash": "",
            "last_login": None
        }

        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, department, position,
            hire_date, base_salary, bonus, currency, annual_leave_balance, sick_leave_balance, performance_rating,
            review_period, last_review_date, password_hash, last_login)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sample_data["employee_id"],
                sample_data["first_name"],
                sample_data["last_name"],
                sample_data["email"],
                sample_data["phone_number"],
                sample_data["department"],
                sample_data["position"],
                sample_data["hire_date"],
                sample_data["base_salary"],
                sample_data["bonus"],
                sample_data["currency"],
                sample_data["annual_leave_balance"],
                sample_data["sick_leave_balance"],
                sample_data["performance_rating"],
                sample_data["review_period"],
                sample_data["last_review_date"],
                sample_data["password_hash"],
                sample_data["last_login"],
            ),
        )
        self.conn.commit()

        # Verify the data has been inserted
        cursor.execute("SELECT * FROM employees WHERE employee_id = 1;")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Data was not inserted into the employees table.")
        self.assertEqual(result[1], "John", "First name does not match.")
        self.assertEqual(result[2], "Doe", "Last name does not match.")

    def test_password_hashing(self):
        """Test if the default password is hashed and updated correctly."""
        default_password = "password123"
        password_hash = hashlib.sha256(default_password.encode()).hexdigest()

        # Update password hash in the test database
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO employees (employee_id, first_name, last_name, email, phone_number, department, position,
            hire_date, base_salary, bonus, currency, annual_leave_balance, sick_leave_balance, performance_rating,
            review_period, last_review_date, password_hash, last_login)
            VALUES (1, 'Test', 'User', 'test.user@example.com', '123-456-7890', 'Engineering', 'Software Engineer',
            '2022-01-01', 70000, 5000, 'USD', 15, 10, 4.5, 'Annual', '2023-01-01', '', NULL)
            """
        )
        self.conn.commit()

        # Hash the password and update
        self.conn.execute(
            """
            UPDATE employees
            SET password_hash = ?
            WHERE employee_id = 1
            """,
            (password_hash,),
        )
        self.conn.commit()

        # Verify the password hash was updated
        cursor.execute("SELECT password_hash FROM employees WHERE employee_id = 1;")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "Password hash was not found.")
        self.assertEqual(result[0], password_hash, "Password hash does not match.")

if __name__ == "__main__":
    unittest.main()
