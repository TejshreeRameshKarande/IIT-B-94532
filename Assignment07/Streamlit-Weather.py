import streamlit as st
import requests
import os
from langchain.chat_models import init_chat_model

st.set_page_config(page_title="Weather App")
st.title("🌤️ Weather Assistant")

# -------- API KEYS --------
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------- LLM --------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# -------- UI --------
city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]

            st.subheader("📊 Raw Weather Data")
            st.write(f"Temperature: {temp} °C")
            st.write(f"Condition: {desc}")
            st.write(f"Humidity: {humidity}%")

            # -------- LLM Explanation --------
            llm_input = f"""
Current weather details:
Temperature: {temp} °C
Condition: {desc}
Humidity: {humidity}%

Explain this weather in very simple English.
"""
            explanation = llm.invoke(llm_input).content
            st.subheader("🧠 AI Explanation")
            st.write(explanation)
        else:
            st.error("City not found or API error")
