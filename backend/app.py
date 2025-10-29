from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import requests
from chroma_client import get_chroma_client, get_collection
import os

# FastAPI App Setup
app = FastAPI(title="RAG Chatbot")

# CORS (so frontend JS can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML templates (for index.html)
templates = Jinja2Templates(directory="templates")

# Ollama & Chroma Configuration
OLLAMA_URL = os.environ.get("OLLAMA_GENERATE_URL", "http://localhost:11434/api/chat")
LLM_MODEL = os.environ.get("OLLAMA_LLM_MODEL", "llama3.2")

# Initialize Chroma client & collection
client = get_chroma_client()
collection = get_collection(client, name="course_materials")

# Exception Handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={"error": str(exc)})

# Serve Frontend
@app.get("/", response_class=HTMLResponse)
def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Query Endpoint
@app.post("/query")
async def query(request: Request):
    """Receives user query, retrieves relevant context, and generates response using Ollama."""
    try:
        data = await request.json()
        query_text = data.get("query", "").strip()

        if not query_text:
            return {"error": "Empty query"}

        #Retrieve from Chroma

        res = collection.query(
            query_texts=query_text,
            n_results=2,
            include=["documents", "metadatas", "distances"]
        )


        if not res.get("documents") or not res["documents"][0]:
            context = "No relevant context found."
        else:
            docs = res["documents"][0]
            metas = res["metadatas"][0]
            context = "\n\n---\n\n".join(
                [f"Source: {m.get('source', 'unknown')} (chunk {m.get('chunk_index', '-')})\n\n{d}"
                 for d, m in zip(docs, metas)]
            )

        #Prompt 
        prompt = f"""
        Use the provided context to answer the user's question.
        If the answer isn't in the context, say "I don't know".

        Context:
        {context}

        User question:
        {query_text}
        """

        #Send to Ollama
        payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
            ],
        "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        #Return Result 
        answer = result.get("message", {}).get("content", "").strip()
        if not answer:
            answer = "No answer found."
        return {"answer": answer}

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
