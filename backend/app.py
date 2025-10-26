# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from chroma_client import get_chroma_client, get_collection
import requests
import os

app = FastAPI()
client = get_chroma_client()
collection = get_collection(client, name="course_materials")

OLLAMA_GENERATE_URL = os.environ.get("OLLAMA_GENERATE_URL", "http://localhost:11434/api/chat")
LLM_MODEL = os.environ.get("OLLAMA_LLM_MODEL", "llama3.2")

class QueryReq(BaseModel):
    query: str
    top_k: int = 2

@app.post("/query")
def query(req: QueryReq):
    # 1) retrieve top-k relevant chunks via Chroma
    res = collection.query(
        query_texts=[req.query],
        n_results=req.top_k,
        include=["documents","metadatas","distances"]
    )
    docs = res['documents'][0]  # list of retrieved text chunks
    metas = res['metadatas'][0]
    distances = res['distances'][0]

    # 2) assemble context
    context = "\n\n---\n\n".join([f"Source: {m['source']} (chunk {m['chunk_index']})\n\n{d}" for d, m in zip(docs, metas)])

    # 3) create a prompt for LLM (you can tailor this)
    prompt = f"""
Use the provided context to answer the user question. If the answer isn't in the context, say "I don't know". 

Context:
{context}

User question:
{req.query}

"""

    # 4) call Ollama chat/generate endpoint
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    r = requests.post(OLLAMA_GENERATE_URL, json=payload)
    r.raise_for_status()
    answer = r.json()
    # response format from /api/chat may be streaming or nested; adapt as needed
    assistant_msg = answer.get("message", {}).get("content") or answer.get("response") or str(answer)

    return {
        "answer": assistant_msg,
        "retrieved": [{"text": d, "meta": m, "distance": dist} for d, m, dist in zip(docs, metas, distances)]
    }
