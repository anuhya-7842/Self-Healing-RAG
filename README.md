# Self-Healing RAG

An AI-powered Retrieval-Augmented Generation (RAG) application built using **LangGraph**, **Google Gemini**, **Sentence Transformers**, **ChromaDB**, and **Streamlit**. The application allows users to upload a PDF, automatically builds a vector database, retrieves relevant information, validates generated responses, and answers questions based only on the uploaded document.

---

## Features

- Upload any PDF document
- Automatic PDF text extraction
- Dynamic text chunking
- Embedding generation using Sentence Transformers
- ChromaDB vector database creation
- Semantic document retrieval
- Answer generation using Google Gemini
- Self-healing workflow with answer validation
- Automatic retry when generated answers are unsupported
- Graceful fallback if relevant information is unavailable
- Interactive Streamlit web interface

---

## Architecture

```
                Upload PDF
                     │
                     ▼
             Extract PDF Text
                     │
                     ▼
             Split into Chunks
                     │
                     ▼
         Generate Embeddings
                     │
                     ▼
            Store in ChromaDB
                     │
                     ▼
               User Question
                     │
                     ▼
          Retrieve Relevant Chunks
                     │
                     ▼
          Generate Answer (Gemini)
                     │
                     ▼
             Critic Validation
              │              │
         Approved         Rejected
              │              │
              ▼              ▼
       Final Answer    Rewrite & Retry
                              │
                              ▼
                     Maximum Retries?
                              │
                     Yes ─────────► Fallback Response
```

---

## Project Structure

```
self-healing-rag/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── pdf_loader.py
│   ├── chunk_docs.py
│   ├── create_vector_db.py
│   └── langgraph_workflow.py
│
├── data/
│
└── chroma_db/
```

---

## Technologies Used

- Python
- Streamlit
- LangGraph
- Google Gemini
- ChromaDB
- Sentence Transformers
- PyPDF

---

## Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## How It Works

1. Upload a PDF document.
2. The application extracts text from the PDF.
3. The text is split into smaller chunks.
4. Embeddings are generated using Sentence Transformers.
5. Chunks are stored in ChromaDB.
6. The user asks a question.
7. Relevant chunks are retrieved.
8. Gemini generates an answer.
9. A critic validates whether the answer is supported by the retrieved context.
10. If validation fails, the workflow retries automatically.
11. If all retries fail, a fallback response is returned.

---

## Example

**Question**

```
What is the title of this document?
```

**Answer**

```
Detecting Mental Disorders in Social Media Through Emotional Patterns – The Case of Anorexia
```

---

## Future Improvements

- Multiple PDF support
- Source citations
- Chat history
- Conversation memory
- Hybrid Search (Keyword + Vector)
- FastAPI backend
- Docker deployment
- User authentication
