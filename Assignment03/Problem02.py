import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(page_title="Weather App")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"

def login_page():
    st.title(" Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == password and username != "":
            st.session_state.page = "weather"
            st.success("Login Successful")
        else:
            st.error("Invalid Login (username must equal password)")

def weather_page():
    st.title(" Weather Page")

    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.write("Temperature:", data["main"]["temp"], "°C")
                st.write("Humidity:", data["main"]["humidity"], "%")
                st.write("Condition:", data["weather"][0]["description"])
            else:
                st.error("City not found")

    if st.button("Logout"):
        st.session_state.page = "thanks"

def thanks_page():
    st.title("🙏 Thank You")
    st.write("You have logged out successfully!")

if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "weather":
    weather_page()
elif st.session_state.page == "thanks":
    thanks_page()