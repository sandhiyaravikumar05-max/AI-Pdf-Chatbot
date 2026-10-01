import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

# Page configuration
st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 AI PDF Chatbot")
st.write("Powered by Ollama Cloud")

st.divider()

# Question box
question = st.text_area(
    "💬 Ask your question:",
    placeholder="Type your question here..."
)

# Ask button
if st.button("Ask AI", use_container_width=True):

    if not question.strip():

        st.warning("Please enter a question.")

    elif not OLLAMA_API_KEY:

        st.error("OLLAMA_API_KEY is not configured.")

    else:

        with st.spinner("🤖 Generating answer..."):

            try:

                response = requests.post(
                    "https://ollama.com/api/chat",

                    headers={
                        "Authorization": f"Bearer {OLLAMA_API_KEY}",
                        "Content-Type": "application/json"
                    },

                    json={
                        "model": "gpt-oss:20b",
                        "messages": [
                            {
                                "role": "user",
                                "content": question
                            }
                        ],
                        "stream": False
                    },

                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                answer = data["message"]["content"]

                st.subheader("🤖 AI Answer")
                st.write(answer)

            except requests.exceptions.RequestException as e:

                st.error(f"API Error: {e}")

            except Exception as e:

                st.error(f"Error: {e}")