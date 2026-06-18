from typing import TypedDict
from urllib import response
from langgraph.graph import StateGraph, END
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv
import chromadb
import os

# Load environment variables
load_dotenv()

# Gemini Client
client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Embedding Model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Persistent ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_collection("rag_docs")


class GraphState(TypedDict):
    query: str
    context: str
    answer: str
    status: str
    retries: int


# -------------------------
# Retriever Node
# -------------------------
def retrieve(state: GraphState):

    print("\n[RETRIEVE]")
    print("Query:", state["query"])

    query_embedding = embedding_model.encode(state["query"])

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3
    )

    docs = results["documents"][0]

    context = "\n".join(docs)

    print("Retrieved Context:")
    print(context)

    return {
        "context": context
    }

# -------------------------
# Generator Node (Gemini)
# -------------------------
def generate(state: GraphState):

    print("\n[GENERATE]")
    print("Generating answer...")

    # Intentionally wrong answer on first attempt
    if state["retries"] == 0:
        answer = "LangGraph was created by Google in 2025."

        print("Generated Answer:", answer)

        return {
            "answer": answer
        }

    prompt = f"""
You are a RAG assistant.

Use ONLY the information provided in the context.

If the answer is not present in the context, say:
"I don't have enough information."

Context:
{state['context']}

Question:
{state['query']}

Answer:
"""

    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    answer = response.text.strip()

    print("Generated Answer:", answer)

    return {
        "answer": answer
    }

# -------------------------
# Critic Node (Gemini)
# -------------------------
def critic(state: GraphState):

    print("\n[CRITIC]")
    print("Evaluating answer...")

    prompt = f"""
You are an AI evaluator.

Context:
{state["context"]}

Answer:
{state["answer"]}

If the answer is supported by the context, reply with only:

approved

Otherwise reply with only:

rejected
"""
    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    verdict = response.text.strip().lower()

    print("Critic Verdict:", verdict)

    if "approved" in verdict:
        return {"status": "approved"}

    return {"status": "rejected"}


# -------------------------
# Query Rewriter Node
# -------------------------
def rewrite_query(state: GraphState):

    print("\n[REWRITE QUERY]")
    print("Original Query:", state["query"])

    prompt = f"""
Rewrite the following query to improve document retrieval.

Query:
{state['query']}

Return only the rewritten query.
"""

    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    new_query = response.text.strip()

    print("Rewritten Query:", new_query)

    return {
        "query": new_query,
        "retries": state["retries"] + 1
    }

def fallback(state: GraphState):

    print("\n[FALLBACK]")
    print("Maximum retries reached.")

    return {
        "answer": "I don't have enough information in the knowledge base to answer this question.",
        "status": "failed"
    }


# -------------------------
# Routing Logic
# -------------------------
def route_after_critic(state: GraphState):

    if state["status"] == "approved":
        return END

    if state["retries"] >= 3:
        return "fallback"

    return "rewrite_query"


# -------------------------
# Build Graph
# -------------------------
workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("critic", critic)
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("fallback", fallback)

workflow.set_entry_point("retrieve")
workflow.add_edge("fallback", END)

workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "critic")

workflow.add_conditional_edges(
    "critic",
    route_after_critic
)

workflow.add_edge("rewrite_query", "retrieve")

graph = workflow.compile()


# -------------------------
# Execute Workflow
# -------------------------
if __name__ == "__main__":

    query = input("Ask a question: ")

    result = graph.invoke(
        {
            "query": query,
            "context": "",
            "answer": "",
            "status": "",
            "retries": 0
        }
    )

    print("\nFINAL RESULT")
    print("=" * 50)
    print("Query:", result["query"])
    print("Answer:", result["answer"])
    print("Status:", result["status"])