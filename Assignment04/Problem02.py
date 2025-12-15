import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ---------------- Files ----------------
USERS_FILE = "users.csv"
HISTORY_FILE = "userfiles.csv"

# ---------------- Initialize CSVs ----------------
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["userid", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["userid", "csv_file", "upload_time"]).to_csv(HISTORY_FILE, index=False)

# ---------------- Session ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "userid" not in st.session_state:
    st.session_state.userid = None

# ---------------- Sidebar Menu ----------------
if not st.session_state.authenticated:
    choice = st.sidebar.selectbox("Menu", ["Home", "Login", "Register"])
else:
    choice = st.sidebar.selectbox("Menu", ["Explore CSV", "See History", "Logout"])

# ---------------- Pages ----------------
def home():
    st.title("Home")
    st.write("Welcome! Please Login or Register.")


def register():
    st.title("Register")
    uid = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Register"):
        users = pd.read_csv(USERS_FILE)
        if uid in users["userid"].values:
            st.error("User already exists")
        else:
            users.loc[len(users)] = [uid, pwd]
            users.to_csv(USERS_FILE, index=False)
            st.success("Registration successful")


def login():
    st.title("Login")
    uid = st.text_input("User ID")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv(USERS_FILE)
        valid = users[(users.userid == uid) & (users.password == pwd)]
        if not valid.empty:
            st.session_state.authenticated = True
            st.session_state.userid = uid
            st.success("Login successful")
        else:
            st.error("Invalid credentials")


def explore_csv():
    st.title("Explore CSV")
    file = st.file_uploader("Upload CSV file", type="csv")

    if file is not None:
        df = pd.read_csv(file)
        st.dataframe(df)

        history = pd.read_csv(HISTORY_FILE)
        history.loc[len(history)] = [
            st.session_state.userid,
            file.name,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]
        history.to_csv(HISTORY_FILE, index=False)


def see_history():
    st.title("Upload History")
    history = pd.read_csv(HISTORY_FILE)
    user_data = history[history.userid == st.session_state.userid]
    st.dataframe(user_data)


def logout():
    st.session_state.authenticated = False
    st.session_state.userid = None
    st.success("Logged out successfully")

# ---------------- Routing ----------------
if choice == "Home":
    home()
elif choice == "Register":
    register()
elif choice == "Login":
    login()
elif choice == "Explore CSV":
    explore_csv()
elif choice == "See History":
    see_history()
elif choice == "Logout":
    logout()