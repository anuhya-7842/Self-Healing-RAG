# Self-Healing RAG with LangGraph

## Overview

This project implements a **Self-Healing Retrieval-Augmented Generation (RAG)** pipeline using **LangGraph**, **ChromaDB**, **Sentence Transformers**, and **Google Gemini**.

Unlike a traditional RAG system, this pipeline does not blindly trust the generated answer. It evaluates its own response using a critic agent and automatically retries retrieval with a reformulated query when the answer is not grounded in the retrieved documents.

---

## Features

- PDF document ingestion
- Text chunking
- Vector embeddings using Sentence Transformers
- ChromaDB vector store
- Semantic document retrieval
- Answer generation using Gemini
- Critic agent for hallucination detection
- Query rewriting and retry mechanism
- Graceful fallback when information is unavailable
- Stateful workflow using LangGraph

---

## Architecture

```text
User Query
    ↓
Retrieve Documents
    ↓
Generate Answer
    ↓
Critic Evaluation
    ↓
Approved? ── Yes → Final Answer
    │
    No
    ↓
Rewrite Query
    ↓
Retrieve Again
    ↓
Generate Again
    ↓
Fallback Response (if retries exceeded)
```

---

## Project Structure

```text
self-healing-rag/
│
├── data/
│   └── LangGraph V1 Essentials.pdf
│
├── src/
│   ├── pdf_loader.py
│   ├── chunk_docs.py
│   ├── vector_store.py
│   ├── retrieve_test.py
│   ├── rag_generator.py
│   ├── critic.py
│   ├── query_rewriter.py
│   ├── workflow.py
│   └── langgraph_workflow.py
│
├── requirements.txt
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/anuhya-7842/self-healing-rag.git
cd self-healing-rag
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Gemini API Key

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run the Pipeline

### Load PDF

```bash
python src/pdf_loader.py
```

### Create Chunks

```bash
python src/chunk_docs.py
```

### Build Vector Store

```bash
python src/vector_store.py
```

### Test Retrieval

```bash
python src/retrieve_test.py
```

### Run Self-Healing RAG Workflow

```bash
python src/langgraph_workflow.py
```

---

## Example Workflow

### Query

```text
What is LangGraph?
```

### Retrieval

Relevant document chunks are retrieved from ChromaDB.

### Generation

Gemini generates an answer.

### Critic Evaluation

The critic checks whether the answer is supported by the retrieved context.

### Retry

If the answer is hallucinated:

- Query is rewritten
- Retrieval is performed again
- A new answer is generated

### Fallback

If all retries fail:

```text
I don't have enough information in the knowledge base to answer this question.
```

---

## Technologies Used

- Python
- LangGraph
- ChromaDB
- Google Gemini
- Sentence Transformers
- PyPDF

---

## Future Improvements

- Streamlit UI
- FastAPI Backend
- Multi-PDF Support
- Source Citations
- Hybrid Search (BM25 + Vector Search)
- Human-in-the-Loop Approval
- Persistent Memory
