import streamlit as st
import time
from .config import client

# Function to integrate LLM like GPT
def query_llm(client_data=None, guest_mode=None):
    
    if not guest_mode: 
        # Create system prompt
        system_message = f"""
        You are an assistant helping non-technical employees with their questions using the information provided.
        
        Employee information:
        - Employee ID: {client_data['employee_id']}
        - Name: {client_data['first_name']} {client_data['last_name']}
        - Department: {client_data['department_name']}
        - Position: {client_data['position_name']}
        - Base Salary: {client_data['base_salary']}
        - Bonus: {client_data['bonus']}
        - Hire Date: {client_data['hire_date']}
        - Performance Rating: {client_data.get('performance_rating', 'N/A')}
        - Review Period: {client_data.get('review_period', 'N/A')}
        - Last Review Date: {client_data.get('last_review_date', 'N/A')}
        - Leave Balance: {client_data.get('annual_leave_balance', 'N/A')} days
        - Sick Leave Balance: {client_data.get('sick_leave_balance', 'N/A')} days
        - Last Login: {client_data.get('last_login', 'N/A')}
        
        You are NOT ALLOWED to answer any question that is not related to the information provided.
        """
    else:
        # Create system prompt
        system_message = f"""
        You are an assistant helping non-technical employees with their questions using the information provided.
        
        You are NOT ALLOWED to answer any question that is not related to the information provided.
        """

    # Get user input
    user_input = st.chat_input("What is your question?")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get AI response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            messages = [
                {"role": "system", "content": system_message},
                *st.session_state.messages
            ]
            
            response = client.chat.completions.create(
                model="gpt-4",  # or your preferred model
                messages=messages,
                stream=True
            )

            # Stream the response
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    return st.session_state.messages