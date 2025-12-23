import os
import mysql.connector
import pandas as pd
import streamlit as st
from langchain.chat_models import init_chat_model

# ---------------- LLM SETUP ----------------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="MySQL NL → SQL Assistant", layout="wide")
st.title("🐬 MySQL Natural Language Query Assistant")

# ---------------- DATABASE INPUT ----------------
st.sidebar.header("🔐 MySQL Connection")

host = st.sidebar.text_input("Host", "localhost")
user = st.sidebar.text_input("Username", "root")
password = st.sidebar.text_input("Password", type="password")
database = st.sidebar.text_input("Database", "mobiledb")

connect_btn = st.sidebar.button("Connect")

# ---------------- SESSION STATE ----------------
if "conn" not in st.session_state:
    st.session_state.conn = None

if "schema" not in st.session_state:
    st.session_state.schema = None

# ---------------- CONNECT TO MYSQL ----------------
if connect_btn:
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        st.session_state.conn = conn
        st.success("✅ Connected to MySQL database")

        # Fetch schema
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        schema_info = ""
        for (table_name,) in tables:
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            schema_info += f"\nTable: {table_name}\n"
            for col in columns:
                schema_info += f"- {col[0]} ({col[1]})\n"

        st.session_state.schema = schema_info
        cursor.close()

    except Exception as e:
        st.error(f"❌ Connection failed: {e}")

# ---------------- SHOW SCHEMA ----------------
if st.session_state.schema:
    st.subheader("📘 Database Schema")
    st.text(st.session_state.schema)

# ---------------- QUESTION INPUT ----------------
if st.session_state.conn:
    st.subheader("💬 Ask a Question")

    question = st.text_input("Enter your question (e.g., Show top 5 employees by salary)")

    if st.button("Generate & Execute SQL") and question:
        # -------- PROMPT TO LLM --------
        prompt = f"""
You are an expert MySQL assistant.

Database schema:
{st.session_state.schema}

User question:
{question}

Rules:
- Generate ONLY a MySQL SELECT query
- Do NOT use markdown or code blocks
- Do NOT explain
- If query is not possible, return Error
"""

        response = llm.invoke(prompt)
        sql_query = response.content.strip()

        st.subheader("🧾 Generated SQL Query")
        st.code(sql_query, language="sql")

        # -------- EXECUTE QUERY --------
        if sql_query.lower().startswith("select"):
            try:
                df = pd.read_sql(sql_query, st.session_state.conn)
                st.subheader("📊 Query Result")
                st.dataframe(df)

                # -------- EXPLANATION --------
                explain_prompt = f"""
Explain the following SQL result in very simple English.

Question:
{question}

Result:
{df}
"""
                explanation = llm.invoke(explain_prompt).content

                st.subheader("🧠 Explanation")
                st.write(explanation)

            except Exception as e:
                st.error(f"❌ SQL Execution Error: {e}")
        else:
            st.error("⚠️ Only SELECT queries are allowed")