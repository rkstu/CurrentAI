import streamlit as st
from app.utils import get_query_and_response
from app.models import TiDBDatabaseComponent

# Initialize the database component
db_component = TiDBDatabaseComponent()

# Session state to store the logged-in user and chat history
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
    st.session_state['first_name'] = None
    st.session_state['chat_history'] = []

def show_signup():
    st.title("Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    
    if st.button("Signup"):
        user_id = db_component.add_user(email, password, first_name, last_name)
        if user_id:
            st.session_state['user_id'] = user_id
            st.session_state['first_name'] = first_name
            st.success(f"User created with ID: {user_id}")
            st.experimental_rerun()  # Redirect to chat after signup
        else:
            st.error("Signup failed. Please try again.")

def show_login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if db_component.user_exists(email, password):
            st.session_state['user_id'] = db_component.get_user_id_by_email(email)
            st.session_state['first_name'] = db_component.get_first_name_by_email(email)
            st.success(f"Welcome, {st.session_state['first_name']}!")
            st.experimental_rerun()  # Redirect to chat after login
        else:
            st.error("Invalid email or password.")
    st.write("[Forgot Password?](#forgot-password)", unsafe_allow_html=True)

def show_forgot_password():
    st.title("Forgot Password")
    email = st.text_input("Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Update Password"):
        user_id = db_component.get_user_id_by_email(email)
        if user_id:
            db_component.update_user_password(user_id, new_password)
            st.success("Password updated successfully.")
        else:
            st.error("Email not found.")

def show_chat():
    st.title("Chat with CurrentAI")
    
    if st.session_state['first_name']:
        st.write(f"Hi, {st.session_state['first_name']}!")
    else:
        st.write("Hi!")
    
    user_query = st.text_area("Ask your question here")
    
    if st.button("Ask"):
        response = get_query_and_response(user_query)
        st.session_state['chat_history'].append((user_query, response))
        st.write("Response:", response)
    
    if len(st.session_state['chat_history']) > 0:
        if st.button("Save Conversation"):
            if st.session_state['user_id']:
                db_component.add_queries(st.session_state['user_id'], st.session_state['chat_history'])
                st.session_state['chat_history'] = []  # Clear chat history after saving
                st.success("Conversation saved.")
            else:
                st.error("Please login to save your conversation.")
                st.experimental_rerun()

def show_logout():
    if st.sidebar.button("Logout", key="logout_button", help="Logout and clear session"):
        st.session_state['user_id'] = None
        st.session_state['first_name'] = None
        st.session_state['chat_history'] = []
        st.experimental_rerun()  # Redirect to the default (Chat) page

def main():
    st.sidebar.title("Navigation")
    
    if st.session_state['user_id']:
        st.sidebar.write(f"Hi, {st.session_state['first_name']}")
        if st.sidebar.button("Chat", key="chat_button", help="Go to chat", 
                             use_container_width=True, 
                             style="background-color: #4CAF50; color: white;"):
            show_chat()
        show_logout()  # Display the logout button
    else:
        if st.sidebar.button("Signup", key="signup_button", help="Go to signup", 
                             use_container_width=True, 
                             style="background-color: #2196F3; color: white;"):
            show_signup()
        if st.sidebar.button("Login", key="login_button", help="Go to login", 
                             use_container_width=True, 
                             style="background-color: #2196F3; color: white;"):
            show_login()

    if not st.session_state['user_id']:
        show_chat()

if __name__ == "__main__":
    main()
