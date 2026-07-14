from pyexpat import model

import chromadb

from sentence_transformers import SentenceTransformer
from pdf_loader import load_pdf
from chunk_docs import chunk_text

embedding_model = None

def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return embedding_model


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

    model = get_embedding_model()
    embeddings = model.encode(chunks)

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

    return collection