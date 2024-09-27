import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Negotiation Chatbot",
    page_icon=":brain:",
    layout="centered",
)

# Check for API key (if needed)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("API key not found. Please ensure the .env file contains the correct key.")
else:
    st.title("Negotiation Chatbot")

    # API URL
    FLASK_API_URL = "http://localhost:5000/chat"

    # State variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Chat interface
    user_input = st.text_input("Type your message here...", key="input")

    if user_input:
        response = requests.post(FLASK_API_URL, json={"input": user_input})
        if response.ok:
            data = response.json()
            bot_response = data['response']

            # Update chat history with the new messages
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", bot_response))

            # Display chat history
            for sender, message in st.session_state.chat_history:
                if sender == "You":
                    st.write(f"You: {message}")
                else:
                    st.write(f"Bot: {message}")
        else:
            st.error("Error communicating with the Flask API.")
