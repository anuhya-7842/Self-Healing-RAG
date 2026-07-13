import streamlit as st
import sys
import tempfile
import os

# Allow importing from src folder
sys.path.append("src")

from create_vector_db import create_vector_db
from langgraph_workflow import graph, load_collection

st.set_page_config(
    page_title="Self-Healing RAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Self-Healing RAG")
st.write("Upload any PDF and ask questions about it.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Upload a single PDF (uploading another PDF will replace the previous one)",
    type=["pdf"]
)

# Question
query = st.text_input("Ask a question")

if st.button("Ask"):

    if uploaded_file is None:
        st.warning("Please upload a PDF.")
        st.stop()

    if query.strip() == "":
        st.warning("Please enter a question.")
        st.stop()

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    # Create fresh vector database
    with st.spinner("Creating knowledge base..."):
        create_vector_db(pdf_path)
    load_collection()

    # Delete temporary PDF
    os.remove(pdf_path)

    # Ask question
    with st.spinner("Thinking..."):

        result = graph.invoke(
            {
                "query": query,
                "context": "",
                "answer": "",
                "status": "",
                "retries": 0
            }
        )

    st.success("Completed!")

    st.subheader("Final Query")
    st.write(result["query"])

    st.subheader("Retrieved Context")
    st.write(result["context"])

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Status")
    st.write(result["status"])

    st.subheader("Retries")
    st.write(result["retries"])