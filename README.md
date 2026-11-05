# Self-Healing RAG

AI-powered PDF question answering system with self-healing Retrieval-Augmented Generation (RAG). Users can upload PDFs, extract and index content, retrieve relevant information, and receive grounded answers using LangGraph, Google Gemini, ChromaDB, and Streamlit. The system validates generated responses and retries automatically when necessary, improving reliability and reducing unsupported answers.

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

---

### 1. Application Homepage
![Application Homepage](screenshots/01-homepage.png)

### 2. PDF Upload
![PDF Upload](screenshots/02-pdf-upload.png)

### 3. Question and Answer Generation
![Question and Answer](screenshots/03-question-answer.png)

### 4. Retrieved Context
![Retrieved Context](screenshots/04-retrieved-context.png)

### 5. LangGraph Workflow
![LangGraph Workflow](screenshots/05-langgraph-workflow.png)

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

## Prerequisites

- Python 3.10 or later
- Git
- A Google Gemini API key
- An internet connection (the embedding model may be downloaded the first time the app runs)

## Installation

1. Clone the repository and move into the project directory:

   ```bash
   git clone https://github.com/anuhya-7842/Self-Healing-RAG.git
   cd Self-Healing-RAG
   ```

2. Create and activate a virtual environment:

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows (PowerShell)**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configure your Gemini API key

Create a `.env` file in the project root, alongside `app.py`, and add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own key. Keep it private and do not commit the `.env` file to Git; it is already listed in `.gitignore`.

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

- Support multiple documents and cite source passages.
- Preserve chat history for follow-up questions.
- Improve retrieval with hybrid search.
- Add deployment and access controls.
