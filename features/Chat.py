import streamlit as st
from app.utils import queries_and_response

def chat():
    st.title("ChatGPT-like Interface")
    user_query = st.text_input("Ask your question:")

    if st.button("Ask"):
        response = queries_and_response(user_query)
        st.write("Response:", response)

if __name__ == "__main__":
    chat()
