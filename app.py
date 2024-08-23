import streamlit as st
import pandas as pd
from io import StringIO
from app.utils import get_query_and_response
from app.models import TiDBDatabaseComponent

# Initialize the database component
db_component = TiDBDatabaseComponent()

# Session state to store the logged-in user and chat history
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
    st.session_state['first_name'] = None
    st.session_state['chat_history'] = []
    st.session_state['current_page'] = 'chat'  # Default to chat

def redirect_to_page(page):
    st.session_state['current_page'] = page
    st.rerun()  # Force rerun to update the page

def fetch_conversation_history(user_id):
    """Fetch the conversation history from the database for the logged-in user."""
    conversation_history = db_component.get_user_queries(user_id)
    return conversation_history

def export_conversation_as_csv(conversation_history):
    """Convert conversation history (list of tuples) to CSV format."""
    df = pd.DataFrame(conversation_history, columns=["User Query", "AI Response"])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def show_signup():
    st.title("🔒 Sign Up")

    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    first_name = st.text_input("First Name", key="signup_first_name")
    last_name = st.text_input("Last Name", key="signup_last_name")

    if st.button("Sign Up"):
        if not email or not password or not first_name or not last_name:
            st.error("All fields are required.")
        else:
            user_id = db_component.add_user(email, password, first_name, last_name)
            if user_id:
                st.session_state['user_id'] = user_id
                st.session_state['first_name'] = first_name
                st.success("🎉 You have been registered. Please log in.")
                redirect_to_page('chat')  # Redirect to chat page
            else:
                st.error("🚫 Signup failed. Please try again.")

def show_login():
    st.title("🔑 Log In")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        if not email or not password:
            st.error("Please enter both email and password.")
        else:
            if db_component.user_exists(email, password):
                st.session_state['user_id'] = db_component.get_user_id_by_email(email)
                st.session_state['first_name'] = db_component.get_first_name_by_email(email)
                st.success(f"👋 Welcome, {st.session_state['first_name']}!")
                redirect_to_page('chat')  # Redirect to chat after successful login
            else:
                st.error("🚫 Invalid email or password. Please try again.")

def show_forgot_password():
    st.title("🔄 Forgot Password")

    email = st.text_input("Email", key="forgot_email")
    new_password = st.text_input("New Password", type="password", key="forgot_password")

    if st.button("Update Password"):
        if not email or not new_password:
            st.error("Both email and new password are required.")
        else:
            user_id = db_component.get_user_id_by_email(email)
            if user_id:
                db_component.update_user_password(user_id, new_password)
                st.success("🔑 Password updated successfully. Please log in.")
                redirect_to_page('login')  # Redirect to login page
            else:
                st.error("🚫 Email not found.")

def show_chat():
    st.title("💬 Chat with CurrentAI")

    if st.session_state['first_name']:
        st.write(f"Hello, {st.session_state['first_name']}! 👋")
    else:
        st.write("Hello! 👋")

    user_query = st.text_area("Ask your question here")

    if st.button("Ask"):
        if not user_query.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner('Fetching the best answer for you...'):
                try:
                    response = get_query_and_response(user_query)
                    if not response:
                        response = "Sorry, I couldn't find an answer for you."
                except Exception as e:
                    response = f"An error occurred: {e}"
                st.session_state['chat_history'].append((user_query, response))
                st.write(f"**Answer:** {response}")

    if len(st.session_state['chat_history']) > 0:
        if st.button("Save Conversation"):
            if st.session_state['user_id']:
                db_component.add_queries(st.session_state['user_id'], st.session_state['chat_history'])
                st.session_state['chat_history'] = []  # Clear chat history after saving
                st.success("💾 Conversation saved.")
            else:
                st.error("🚫 Please log in to save your conversation.")

def show_export_button():
    """Show an export button for logged-in users or display an info message for others."""
    st.sidebar.title("🌟 Export Options")
    
    if st.sidebar.button("Export Conversation 📝"):
        if st.session_state['user_id']:
            # Fetch conversation history from the database
            conversation_history = fetch_conversation_history(st.session_state['user_id'])
            
            if conversation_history:
                # Generate CSV for download
                csv_data = export_conversation_as_csv(conversation_history)
                st.sidebar.download_button(
                    label="Download Conversation as CSV 📄",
                    data=csv_data,
                    file_name="conversation_history.csv",
                    mime="text/csv"
                )
            else:
                st.sidebar.info("No conversation history found to export.")
        else:
            st.sidebar.info("🚫 Please log in to export your conversation.")

def show_logout():
    if st.sidebar.button("Logout 🏠", key="logout_button", help="Logout and clear session"):
        st.session_state['user_id'] = None
        st.session_state['first_name'] = None
        st.session_state['chat_history'] = []
        redirect_to_page('chat')  # Redirect to chat on logout

def main():
    st.set_page_config(page_title="CurrentAI", page_icon="🕒")  # Set page title and icon

    st.sidebar.title("🌟 Explore")

    # Always show Chat button in the sidebar
    if st.sidebar.button("Chat 💬", key="sidebar_chat_button", help="Go to chat", use_container_width=True):
        redirect_to_page('chat')

    # Show navigation options based on session state
    if st.session_state['user_id']:
        st.sidebar.write(f"Hi, {st.session_state['first_name']}! 👋")
        show_logout()  # Display the logout button
    else:
        if st.sidebar.button("Sign Up ✍️", key="signup_button", help="Go to sign up", use_container_width=True):
            redirect_to_page('signup')
        if st.sidebar.button("Log In 🔑", key="login_button", help="Go to log in", use_container_width=True):
            redirect_to_page('login')
        if st.sidebar.button("Forgot Password 🔄", key="forgot_button", help="Go to forgot password", use_container_width=True):
            redirect_to_page('forgot_password')

    # Show the export button (with different behavior for logged-in vs non-logged-in users)
    show_export_button()

    # Show the correct page based on session state
    if st.session_state.get('current_page') == 'signup':
        show_signup()
    elif st.session_state.get('current_page') == 'login':
        show_login()
    elif st.session_state.get('current_page') == 'forgot_password':
        show_forgot_password()
    else:
        show_chat()  # Default to chat page

if __name__ == "__main__":
    main()
