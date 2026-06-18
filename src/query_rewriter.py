from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def rewrite_query(query):

    prompt = f"""
Rewrite the following query to improve document retrieval.

Query:
{query}

Return only the rewritten query.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()


if __name__ == "__main__":

    query = "What is LangGraph?"

    rewritten_query = rewrite_query(query)

    print("Original Query:", query)
    print("Rewritten Query:", rewritten_query)