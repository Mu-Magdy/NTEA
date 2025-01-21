import streamlit as st
from helper.chatbot import query_llm
from helper.authentication import authenticate_employee
from helper.data import get_data

def chat_interface(user_data):
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query_llm(user_data)

def main():
    st.title("NTEA Chatbot")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_employee(email, password) == 'User not found':
                st.error('User not found')
            
            elif authenticate_employee(email, password):
                st.session_state.logged_in = True
                st.session_state.ID = authenticate_employee(email, password)
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        user_data = get_data(st.session_state.ID)
        
        if user_data is None:
            st.error("Failed to retrieve user data. Please try logging in again.")
            st.session_state.logged_in = False
            st.rerun()
        
        chat_interface(user_data)

if __name__ == "__main__":
    main()


# # Example usage:
# Email: paulamanda@example.com
        # anthonymeadows@example.net
        # steven46@example.org
        # achristensen@example.org
# PassWord: 123