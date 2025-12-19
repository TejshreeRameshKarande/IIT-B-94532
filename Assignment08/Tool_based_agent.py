import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

# ------------------ ENV ------------------
load_dotenv()

# ------------------ STREAMLIT CONFIG ------------------
st.set_page_config(page_title="LangChain Agent with Tools", layout="centered")
st.title("🧠 LangChain Agent with Tools (Explain / Summarize File)")

# ------------------ FILE UPLOAD ------------------

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
uploaded_text = ""

if uploaded_file is not None:
    uploaded_text = uploaded_file.read().decode("utf-8")
    st.success(f"File '{uploaded_file.name}' uploaded successfully")

# ------------------ TOOLS ------------------

@tool
def calculator(expression: str) -> str:
    """Evaluates a basic arithmetic expression."""
    try:
        return str(eval(expression))
    except Exception:
        return "Error: Invalid expression"


@tool
def read_uploaded_file(_: str = "") -> str:
    """
    Reads content of the uploaded text file.
    """
    if uploaded_text:
        return uploaded_text
    return "Error: No file uploaded"


@tool
def current_weather(city: str) -> str:
    """Gets current weather of a city."""
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )
        response = requests.get(url)
        return json.dumps(response.json())
    except Exception:
        return "Error: Weather not found"


@tool
def knowledge_lookup(topic: str) -> str:
    """Returns short knowledge about a topic."""
    knowledge = {
        "langchain": "LangChain is a framework for building LLM-powered applications.",
        "agent": "An agent decides which tool to use based on user input.",
        "llm": "LLM stands for Large Language Model."
    }
    return knowledge.get(topic.lower(), "No knowledge available")

# ------------------ SESSION STATE ------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "logs" not in st.session_state:
    st.session_state.logs = []

# ------------------ MODEL ------------------

llm = init_chat_model(
    model="microsoft/phi-4-mini-reasoning",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

# ------------------ AGENT ------------------

agent = create_agent(
    model=llm,
    tools=[
        calculator,
        read_uploaded_file,
        current_weather,
        knowledge_lookup
    ],
    system_prompt=(
        "You are a helpful assistant.\n"
        "If the user asks to read, explain, or summarize a text file, "
        "you MUST first use the read_uploaded_file tool to get the file content. "
        "Then explain or summarize the content as requested.\n"
        "Do not say you lack access to files."
    )
)

# ------------------ UI ------------------

user_input = st.text_input("Enter your prompt:")

if st.button("Run Agent") and user_input:
    st.session_state.logs.clear()
    st.session_state.logs.append(f"User input: {user_input}")

    result = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })

    st.session_state.messages = result["messages"]

    # Manual logging
    for msg in result["messages"]:
        if msg.type == "tool":
            st.session_state.logs.append(
                f"Tool executed: {msg.name} | Output preview: {msg.content[:150]}"
            )

    st.subheader("🤖 AI Response")
    st.write(result["messages"][-1].content)

# ------------------ MESSAGE HISTORY ------------------

if st.session_state.messages:
    st.subheader("📜 Message History")
    for msg in st.session_state.messages:
        st.json({
            "type": msg.type,
            "name": getattr(msg, "name", None),
            "content": msg.content
        })

# ------------------ LOG OUTPUT ------------------

if st.session_state.logs:
    st.subheader("🪵 Execution Logs (Manual Middleware)")
    for log in st.session_state.logs:
        st.write(log)