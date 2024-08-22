import streamlit as st
from app.models import TiDBDatabaseComponent

db_component = TiDBDatabaseComponent()

def login():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        exists = db_component.user_exists(email, password)
        if exists:
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

if __name__ == "__main__":
    login()
