import os
import json
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

# ---------------------------------------
# Load .env file (THIS WAS MISSING)
# ---------------------------------------
load_dotenv(Path(__file__).parent / ".env")

# ---------------------------------------
# Read API keys
# ---------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GROQ_API_KEY or not GEMINI_API_KEY:
    raise ValueError("API keys not found in environment variables.")

# ---------------------------------------
# User input
# ---------------------------------------
user_prompt = input("Ask anything: ")

# ---------------------------------------
# GROQ (raw HTTP, sir-style)
# ---------------------------------------
groq_url = "https://api.groq.com/openai/v1/chat/completions"
groq_headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

groq_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

start = time.time()
groq_response = requests.post(
    groq_url,
    headers=groq_headers,
    data=json.dumps(groq_data)
)
groq_time = time.time() - start

groq_result = groq_response.json()["choices"][0]["message"]["content"]

# ---------------------------------------
# GEMINI (raw HTTP, sir-style)
# ---------------------------------------
gemini_url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
    f"?key={GEMINI_API_KEY}"
)

gemini_headers = {
    "Content-Type": "application/json"
}

gemini_data = {
    "contents": [
        {
            "parts": [{"text": user_prompt}]
        }
    ]
}

start = time.time()
gemini_response = requests.post(
    gemini_url,
    headers=gemini_headers,
    data=json.dumps(gemini_data)
)
gemini_time = time.time() - start

gemini_result = gemini_response.json()["candidates"][0]["content"]["parts"][0]["text"]

# ---------------------------------------
# Output
# ---------------------------------------
print("\n--- RESULTS ---")
print(f"Groq Speed   : {groq_time:.2f}s")
print(f"Groq Output  : {groq_result[:200]}...\n")

print(f"Gemini Speed : {gemini_time:.2f}s")
print(f"Gemini Output: {gemini_result[:200]}...")