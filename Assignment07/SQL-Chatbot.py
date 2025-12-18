import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
import os

st.title("CSV -> SQL Chatbot")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("CSV Preview")
    st.dataframe(df.head())

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    question = st.text_input("Ask a question about this CSV")

    if question:
        llm_input = f"""
Table Name: data
Table Schema: {df.dtypes}
Question: {question}
Instruction:
Write a SQL query for the above question.
Generate SQL query only in plain text.
If you cannot generate the query, output 'Error'.
"""

        sql_query = llm.invoke(llm_input).content.strip()
        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        if sql_query.lower() != "error":
            try:
                result_df = sqldf(sql_query, {"data": df})
                st.subheader("Query Result")
                st.dataframe(result_df)

                explain_input = f"""
The SQL query result is:
{result_df.head().to_string(index=False)}

Explain this result in simple English.
"""
                explanation = llm.invoke(explain_input).content
                st.subheader("Explanation")
                st.write(explanation)

            except Exception as e:
                st.error(f"SQL Execution Error: {e}")
