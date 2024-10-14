import os
from openai import OpenAI
from dotenv import load_dotenv


# Load the Key token
_ = load_dotenv(override=True)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


# Function to integrate LLM like GPT
def query_llm(employee_data, user_query):
    # Format the employee data and question for the LLM
    prompt = f"""
    Employee Information: {employee_data}
    
    Question: {user_query}
    """

    client = OpenAI(
        api_key=OPENAI_API_KEY,
    )
    system_message = """
    You are an assistant helping non-technical employees with their questions using the information provided.
    
    You will receive the data about the employee in a list of dictionary
    the variables of the each dictionary are:
        employee_id: Unique identifier for each employee
        first_name: Employee's first name
        last_name: Employee's last name
        email: Employee's email (used for authentication)
        phone_number: Employee's contact number
        department: Employee's department
        position: Job title or position
        hire_date: Date when the employee was hired
        base_salary: Employee's base salary
        bonus: Most recent bonus amount
        currency: Currency of the salary
        annual_leave_balance: Number of annual leave days remaining
        sick_leave_balance: Number of sick leave days remaining
        performance_rating: Latest performance rating (e.g., 4.5)
        review_period: Period of the last review (e.g., Q1, 2024)
        last_review_date: Date of the last performance review
        password_hash: Hashed password for secure authentication
        last_login: Date and time of the last login
    """
    # Send the prompt to the LLM model
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {"role": "user", "content": prompt},
        ],
    )

    # Return the LLM's response
    return response.choices[0].message.content


# Mock LLM function for testing purposes
def query_llm_mock(employee_data: dict, user_query):
    # Create a simple mock response using employee data
    if "salary" in user_query.lower():
        return f"Your salary is {employee_data[5]} with a bonus of {employee_data[6]}."
    elif "leave" in user_query.lower():
        return f"You have {employee_data[7]} annual leave days and {employee_data[8]} sick leave days."
    elif "performance" in user_query.lower():
        return f"Your last performance review was on {employee_data[11]} with a rating of {employee_data[9]}."
    else:
        return "I'm sorry, I couldn't understand your query."
