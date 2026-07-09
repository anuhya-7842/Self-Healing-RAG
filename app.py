import streamlit as st
import sys

# Allow importing from src folder
sys.path.append("src")

from langgraph_workflow import graph

st.set_page_config(
    page_title="Self-Healing RAG",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Self-Healing RAG")
st.write("Ask questions about your uploaded knowledge base.")

query = st.text_input("Ask a question")

if st.button("Ask"):

    if query.strip() == "":
        st.warning("Please enter a question.")
    else:

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