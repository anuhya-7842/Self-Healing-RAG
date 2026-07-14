from typing import TypedDict
from langgraph.graph import StateGraph, END
from sentence_transformers import SentenceTransformer
from google import genai
from dotenv import load_dotenv
import chromadb
import os

from torchgen import model

# -------------------------
# Load Environment Variables
# -------------------------
load_dotenv()

client_gemini = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_model = None

def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return embedding_model

# Global collection
collection = None


def load_collection():
    global collection

    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection("rag_docs")


class GraphState(TypedDict):
    query: str
    context: str
    answer: str
    status: str
    retries: int


# -------------------------
# Retriever
# -------------------------
def retrieve(state: GraphState):

    global collection

    if collection is None:
        load_collection()

    print("\n[RETRIEVE]")
    print("Query:", state["query"])

    model = get_embedding_model()
    query_embedding = model.encode(state["query"])

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
# Generator
# -------------------------
def generate(state: GraphState):

    print("\n[GENERATE]")

    if state["retries"] == 0:
        answer = "LangGraph was created by Google in 2025."

        return {
            "answer": answer
        }

    prompt = f"""
You are a RAG assistant.

Use ONLY the information provided in the context.

If the answer is not present in the context, say:
"I don't have enough information."

Context:
{state["context"]}

Question:
{state["query"]}

Answer:
"""

    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return {
        "answer": response.text.strip()
    }


# -------------------------
# Critic
# -------------------------
def critic(state: GraphState):

    prompt = f"""
You are an AI evaluator.

Context:
{state["context"]}

Answer:
{state["answer"]}

If the answer is supported by the context reply only:

approved

Otherwise reply only:

rejected
"""

    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    verdict = response.text.strip().lower()

    if "approved" in verdict:
        return {"status": "approved"}

    return {"status": "rejected"}


# -------------------------
# Rewrite Query
# -------------------------
def rewrite_query(state: GraphState):

    prompt = f"""
Rewrite the following query to improve document retrieval.

Query:
{state["query"]}

Return only the rewritten query.
"""

    response = client_gemini.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return {
        "query": response.text.strip(),
        "retries": state["retries"] + 1
    }


# -------------------------
# Fallback
# -------------------------
def fallback(state: GraphState):

    return {
        "answer": "I don't have enough information in the knowledge base.",
        "status": "failed"
    }


# -------------------------
# Routing
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

workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "critic")

workflow.add_conditional_edges(
    "critic",
    route_after_critic
)

workflow.add_edge("rewrite_query", "retrieve")
workflow.add_edge("fallback", END)

graph = workflow.compile()


if __name__ == "__main__":

    load_collection()

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

    print(result)