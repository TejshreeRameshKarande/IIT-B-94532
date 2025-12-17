import os
import requests
import streamlit as st
from dotenv import load_dotenv

# ---------------- APP CONFIG ----------------
st.set_page_config(page_title="Groq vs LM Studio Chatbot")
st.title("💬 Multi-LLM Chatbot")

load_dotenv()

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Settings")

llm_choice = st.sidebar.radio(
    "Choose LLM Provider",
    ["Groq (Cloud)", "LM Studio (Local)"]
)

show_history = st.sidebar.checkbox("📜 Show Chat History", value=True)

# ---------------- SESSION STATE ----------------
if "groq_messages" not in st.session_state:
    st.session_state.groq_messages = []

if "lm_messages" not in st.session_state:
    st.session_state.lm_messages = []

# Select active messages
messages = (
    st.session_state.groq_messages
    if llm_choice == "Groq (Cloud)"
    else st.session_state.lm_messages
)

# ---------------- CHAT HISTORY ----------------
if show_history:
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_prompt = st.chat_input("Ask anything...")

if user_prompt:
    messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # ---------------- GROQ (CLOUD) ----------------
    if llm_choice == "Groq (Cloud)":
        try:
            api_key = os.getenv("GROQ_API_KEY")

            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env")

            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            resp = response.json()
            answer = resp["choices"][0]["message"]["content"]

        except Exception as e:
            answer = f"❌ Groq Error: {e}"

    # ---------------- LM STUDIO (LOCAL) ----------------
    else:
        try:
            url = "http://127.0.0.1:1234/v1/chat/completions"
            headers = {"Content-Type": "application/json"}

            payload = {
                "model": "microsoft/phi-4-mini-reasoning",
                "messages": messages,
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            resp = response.json()
            answer = resp["choices"][0]["message"]["content"]

            if isinstance(answer, list):
                answer = answer[0]["text"]

        except Exception:
            answer = "❌ LM Studio server is not running. Start it on port 1234."

    # ---------------- SAVE & DISPLAY ----------------
    messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
