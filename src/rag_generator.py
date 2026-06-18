import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")

# Simulated retrieved document
context = """
LangGraph is a framework for building stateful, multi-agent applications with LLMs.
"""

question = "What is LangGraph?"

prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}
"""

response_text = "LangGraph is a framework for building stateful, multi-agent applications with LLMs."
print(response_text)