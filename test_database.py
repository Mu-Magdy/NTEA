import sqlite3
import pytest

@pytest.fixture
def db_connection():
    conn = sqlite3.connect(':memory:')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT UNIQUE NOT NULL
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS positions (
        position_id INTEGER PRIMARY KEY AUTOINCREMENT,
        position_name TEXT UNIQUE NOT NULL
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone_number TEXT,
        department_id INTEGER,
        position_id INTEGER,
        hire_date TEXT,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (department_id) REFERENCES departments(department_id),
        FOREIGN KEY (position_id) REFERENCES positions(position_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS salaries (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        base_salary REAL,
        bonus REAL,
        currency TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS leaves (
        leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        annual_leave_balance INTEGER,
        sick_leave_balance INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS performance (
        performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        rating REAL,
        review_period TEXT,
        last_review_date TEXT,
        UNIQUE (employee_id, review_period),
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS auth (
        auth_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        password_hash TEXT,
        salt TEXT,
        last_login TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    );
    ''')

    yield cur, conn

    conn.close()


def test_department_insertion(db_connection):
    cur, conn = db_connection
    cur.execute("INSERT INTO departments (department_name) VALUES (?)", ('HR',))
    conn.commit()

    cur.execute("SELECT department_name FROM departments WHERE department_name = 'HR'")
    department = cur.fetchone()
    assert department[0] == 'HR'


def test_position_insertion(db_connection):
    cur, conn = db_connection
    cur.execute("INSERT INTO positions (position_name) VALUES (?)", ('Manager',))
    conn.commit()

    cur.execute("SELECT position_name FROM positions WHERE position_name = 'Manager'")
    position = cur.fetchone()
    assert position[0] == 'Manager'


def test_employee_insertion(db_connection):
    cur, conn = db_connection

    cur.execute("INSERT INTO departments (department_name) VALUES (?)", ('HR',))
    cur.execute("INSERT INTO positions (position_name) VALUES (?)", ('Manager',))
    department_id = cur.lastrowid
    position_id = cur.lastrowid

    cur.execute('''
        INSERT INTO employees (first_name, last_name, email, department_id, position_id) 
        VALUES (?, ?, ?, ?, ?)
    ''', ('John', 'Doe', 'john.doe@example.com', department_id, position_id))
    conn.commit()

    cur.execute("SELECT first_name, last_name, email FROM employees WHERE email = 'john.doe@example.com'")
    employee = cur.fetchone()
    assert employee[0] == 'John'
    assert employee[1] == 'Doe'
    assert employee[2] == 'john.doe@example.com'


def test_salary_insertion(db_connection):
    cur, conn = db_connection

    cur.execute("INSERT INTO employees (first_name, last_name, email) VALUES (?, ?, ?)", ('Alice', 'Smith', 'alice.smith@example.com'))
    employee_id = cur.lastrowid

    cur.execute('''
        INSERT INTO salaries (employee_id, base_salary, bonus, currency) 
        VALUES (?, ?, ?, ?)
    ''', (employee_id, 60000, 5000, 'USD'))
    conn.commit()

    cur.execute("SELECT base_salary, bonus, currency FROM salaries WHERE employee_id = ?", (employee_id,))
    salary = cur.fetchone()
    assert salary[0] == 60000
    assert salary[1] == 5000
    assert salary[2] == 'USD'


def test_leave_insertion(db_connection):
    cur, conn = db_connection

    cur.execute("INSERT INTO employees (first_name, last_name, email) VALUES (?, ?, ?)", ('Bob', 'Johnson', 'bob.johnson@example.com'))
    employee_id = cur.lastrowid

    cur.execute('''
        INSERT INTO leaves (employee_id, annual_leave_balance, sick_leave_balance) 
        VALUES (?, ?, ?)
    ''', (employee_id, 10, 5))
    conn.commit()

    cur.execute("SELECT annual_leave_balance, sick_leave_balance FROM leaves WHERE employee_id = ?", (employee_id,))
    leave = cur.fetchone()
    assert leave[0] == 10
    assert leave[1] == 5
