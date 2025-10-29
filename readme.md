RAG Chatbot : PDF Knowledge Retrieval

A Retrieval-Augmented Generation (RAG) application that allows semantic search and contextual Q&A over academic course PDFs using ChromaDB and Ollama embeddings.
This project demonstrates how to build a subject specific chatbot for academic knowledge retrieval.

Features
1. PDF Ingestion – Upload and index course PDFs.
2. Chunking – Splits PDFs into manageable chunks for semantic search.
3. Vector Store – Uses ChromaDB for embeddings and retrieval.
4. Contextual Q&A – Uses Ollama (LLM) to answer questions with context from PDFs.
5. Chat Interface – Simple web-based interface for querying course material.
6. Extensible – Easily extendable to multiple subjects or course materials.

Tech Stack
1. Backend: Python, FastAPI
2. Vector Database: ChromaDB
3. Embeddings: Ollama LLM embeddings
4. Frontend: HTML, TailwindCSS, Vanilla JS
5. PDF Parsing: PyMuPDF (fitz)
6. HTTP Requests: requests library

Project Structure
Backend/
│
├── app.py              # FastAPI backend
├── ingest.py           # PDF ingestion & embedding script
├── pdf_utils.py        # PDF text extraction & chunking
├── templates/
│   └── index.html      # Chat interface
└── static/
    └── app.js          # JS frontend logic

Getting Started
1️Clone the repository: 
git clone https://github.com/Suyoga/Rag-Chatbot.git
cd Rag-Chatbot/Backend
2️Create virtual environment & install dependencies: 
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

3️Run Ollama LLM
Ensure Ollama is installed and the model is pulled:
i. ollama list               # Check available models
ii. ollama pull llama3.2      # Pull if not available
iii. ollama serve              # Start Ollama server

4️Ingest PDFs
python ingest.py --pdf /path/to/course.pdf
This will split the PDF into chunks and store embeddings in ChromaDB.

5️Run the Backend
uvicorn app:app --reload
Backend will run on http://127.0.0.1:8000.

6️Open Frontend
Visit in your browser:
http://127.0.0.1:8000
Type a question in the input box.
Bot will reply based on the uploaded PDFs.

Notes:
1. Adjust chunk size and overlap in pdf_utils.py to optimize search quality.
2. The system currently supports single-document ingestion, but you can extend it for multiple PDFs.
3. Ensure Ollama server is running before querying; otherwise, the frontend will show "Load failed".

Future Improvements:
1. Add file upload from frontend.
2. Add streaming responses from Ollama for faster feedback.
3. Support multi-subject retrieval with multiple collections.
4. Integrate user authentication for private course material.

Suyoga Srinivas
