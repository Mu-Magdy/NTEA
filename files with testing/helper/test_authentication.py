import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import hashlib
import pandas as pd
import os

# Import the function to be tested
from your_module_name import authenticate_employee  # Replace with the actual module name

class TestEmployeeAuthentication(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_authenticate_employee_success(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock the database return value
        email = 'test@example.com'
        password = 'password123'
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        mock_cursor.fetchone.return_value = (1, 'John', 'Doe', email, password_hash)
        
        # Call the function
        result = authenticate_employee(email, password)
        
        # Check the result
        expected_result = [{'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'email': email, 'password_hash': password_hash}]
        self.assertEqual(result, expected_result)
        print("Test passed: Authentication successful.")

    @patch('sqlite3.connect')
    def test_authenticate_employee_failure(self, mock_connect):
        # Mock the database connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        # Mock the database return value for failed authentication
        email = 'wrong@example.com'
        password = 'wrongpassword'
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        mock_cursor.fetchone.return_value = None
        
        # Call the function
        result = authenticate_employee(email, password)
        
        # Check the result
        self.assertIsNone(result)
        print("Test passed: Authentication failed as expected.")

if __name__ == '__main__':
    unittest.main()
