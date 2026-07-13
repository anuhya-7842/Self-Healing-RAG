import chromadb

from sentence_transformers import SentenceTransformer
from pdf_loader import load_pdf
from chunk_docs import chunk_text

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def create_vector_db(pdf_path):

    client = chromadb.PersistentClient(path="chroma_db")

    # Delete old collection if it exists
    try:
        client.delete_collection("rag_docs")
    except:
        pass

    # Create fresh collection
    collection = client.create_collection("rag_docs")

    text = load_pdf(pdf_path)

    chunks = chunk_text(text)

    embeddings = embedding_model.encode(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

    return collection