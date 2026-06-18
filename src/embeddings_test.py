from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "LangGraph is a framework for building stateful applications.",
    "RAG combines retrieval with generation."
]

embeddings = model.encode(texts)

print("Number of embeddings:", len(embeddings))
print("Embedding dimension:", len(embeddings[0]))