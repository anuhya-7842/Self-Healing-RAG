from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Load collection
collection = client.get_collection("rag_docs")

# Query
query = "What is LangGraph?"

query_embedding = model.encode(query)

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=3
)

print("\nRetrieved Documents:\n")

for doc in results["documents"][0]:
    print(doc)
    print("-" * 50)