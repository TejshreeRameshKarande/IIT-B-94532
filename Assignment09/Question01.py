import streamlit as st
import pandas as pd
from pandasql import sqldf
import os
import time
import tempfile

from langchain.chat_models import init_chat_model

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# =====================================================
# INITIALIZE LLM (GROQ)
# =====================================================
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================================
# STREAMLIT PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Multi-Agent Intelligent App", layout="wide")
st.title("🤖 Multi-Agent Intelligent Application")

# =====================================================
# SESSION STATE
# =====================================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "web_df" not in st.session_state:
    st.session_state.web_df = None

# =====================================================
# SIDEBAR: CHAT HISTORY (QUESTIONS ONLY)
# =====================================================
st.sidebar.title("💬 Chat History (Questions Only)")

if not st.session_state.chat_history:
    st.sidebar.info("No questions asked yet")
else:
    for agent, question in st.session_state.chat_history:
        st.sidebar.markdown(f"**{agent}:**")
        st.sidebar.markdown(f"- {question}")
        st.sidebar.markdown("---")

# =====================================================
# AGENT 1: CSV QUESTION ANSWERING AGENT
# =====================================================
st.header("📄 CSV Question Answering Agent")

csv_file = st.file_uploader("Upload CSV File", type=["csv"])

if csv_file:
    df = pd.read_csv(csv_file)

    st.subheader("CSV Schema")
    st.write(df.dtypes)

    csv_question = st.text_input("Ask a question about the CSV data")

    if st.button("Ask CSV Agent"):
        st.session_state.chat_history.append(
            ("CSV Agent", csv_question)
        )

        llm_prompt = f"""
        Table Name: data
        Table Schema: {df.dtypes}
        Question: {csv_question}

        Instruction:
        Write ONLY SQL query.
        Do NOT use markdown.
        Do NOT explain.
        """

        raw_sql = llm.invoke(llm_prompt).content
        sql_query = raw_sql.replace("```sql", "").replace("```", "").strip()

        st.code(sql_query, language="sql")

        try:
            result = sqldf(sql_query, {"data": df})
            st.dataframe(result)

            explanation = llm.invoke(
                f"Explain this result in simple English:\n{result}"
            ).content

            st.success(explanation)

        except Exception as e:
            st.error(f"SQL Error: {e}")

# =====================================================
# AGENT 2: SUNBEAM WEB SCRAPING AGENT (FIXED)
# =====================================================
st.header("🌐 Web Scraping Agent (Sunbeam Internship Data)")

if st.button("Scrape Sunbeam Internship Data"):
    temp_dir = tempfile.mkdtemp()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        driver.get("https://www.sunbeaminfo.in/internship")
        time.sleep(3)

        rows = driver.find_elements(By.XPATH, "//table//tr[td]")

        scraped_data = []

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:
                batch_name = cols[1].text.strip()
                start_date = cols[2].text.strip()

                if batch_name or start_date:
                    scraped_data.append({
                        "Batch Name": batch_name,
                        "Start Date": start_date
                    })

        st.session_state.web_df = pd.DataFrame(scraped_data)

    finally:
        driver.quit()

# =====================================================
# WEB DATA QA
# =====================================================
if st.session_state.web_df is not None:
    st.subheader("Scraped Internship Data")
    st.dataframe(st.session_state.web_df)

    web_question = st.text_input("Ask a question about Sunbeam internships")

    if st.button("Ask Web Agent"):
        st.session_state.chat_history.append(
            ("Web Scraping Agent", web_question)
        )

        answer = llm.invoke(
            f"""
            Data:
            {st.session_state.web_df}

            Question:
            {web_question}

            Explain the answer in simple English.
            """
        ).content

        st.success(answer)
