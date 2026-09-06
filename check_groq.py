import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

key = os.getenv("GROQ_API_KEY", "")
model = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

print(f"Testing Key: '{key[:8]}...' with model: '{model}'")

try:
    llm = ChatGroq(groq_api_key=key, model=model, temperature=0.0)
    res = llm.invoke("Hello, respond with one word: Success.")
    print(f"\n✅ Groq Connection Successful!\nResponse: {res.content}")
except Exception as e:
    print(f"\n❌ Groq Execution Error:\n{e}")