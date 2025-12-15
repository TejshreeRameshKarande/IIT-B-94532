import streamlit as st
import time

# Store chat messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Settings")
    choices = ["Upper", "Lower", "Toggle"]
    mode = st.selectbox("Select Mode", choices)
    count = st.slider("Message Count", min_value=2, max_value=10, value=6, step=2)

    st.subheader("Config")
    st.json({"mode": mode, "count": count})

st.title("Sunbeam Chatbot")

def stream_reply(text):
    for ch in text:
        yield ch
        time.sleep(0.05)   

msg = st.chat_input("Say something...")

if msg:
    if mode == "Upper":
        outmsg = msg.upper()
    elif mode == "Lower":
        outmsg = msg.lower()
    elif mode == "Toggle":
        outmsg = msg.swapcase()

    st.session_state.messages.append(("human", msg))
    st.session_state.messages.append(("ai", outmsg))

#chat history
for role, message in st.session_state.messages:
    with st.chat_message(role):
        if role == "ai":
            st.write_stream(stream_reply(message))
        else:
            st.write(message)