from authentication import authenticate_employee
from llm import query_llm, query_llm_mock

# Example of using this function in chatbot interaction
def chatbot_interaction_with_llm(email, password, query):
    # Authenticate the employee
    employee_df = authenticate_employee(email, password)

    if len(employee_df):
        # Query the LLM with the employee's information and query
        response = query_llm(employee_df, query)
        print(f"Chatbot Response: {response}")
    else:
        print("Authentication failed. Please try again.")


# Use the mock LLM function in chatbot interaction
def chatbot_interaction_with_mock_llm(email, password, query):
    # Authenticate the employee
    employee = authenticate_employee(email, password)
    
    if len(employee):
        # Query the mock LLM with the employee's information and query
        response = query_llm_mock(employee, query)
        print(f"Chatbot Response: {response}")
    else:
        print("Authentication failed. Please try again.")


chatbot_interaction_with_llm(email="xperry@gmail.com",
                                password="password123",
                                query="مرتبي كام؟")