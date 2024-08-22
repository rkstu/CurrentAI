import streamlit as st
from app.models import TiDBDatabaseComponent

db_component = TiDBDatabaseComponent()

def signup():
    st.title("Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")

    if st.button("Sign Up"):
        user_id = db_component.add_user(email, password, first_name, last_name)
        st.success(f"User created successfully! Your user ID: {user_id}")

if __name__ == "__main__":
    signup()
