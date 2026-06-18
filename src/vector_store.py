from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# -------------------------
# Load PDF
# -------------------------
pdf_path = r"data/LangGraph V1 Essentials.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

# -------------------------
# Create Chunks
# -------------------------
chunk_size = 500

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

print("Total Chunks:", len(chunks))

# -------------------------
# Embedding Model
# -------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(chunks)

# -------------------------
# ChromaDB
# -------------------------
client = chromadb.PersistentClient(path="./chroma_db")

# Delete old collection
try:
    client.delete_collection("rag_docs")
    print("Old collection deleted.")
except:
    pass

collection = client.create_collection("rag_docs")

# -------------------------
# Store Chunks
# -------------------------
for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embedding.tolist()]
    )

print("PDF chunks stored successfully!")