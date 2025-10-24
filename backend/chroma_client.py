# chroma_client.py
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
import os

# persistent client (store on disk; good for demos)
CHROMA_DIR = os.environ.get("CHROMA_DIR", "./chroma_data")

def get_chroma_client():
    # PersistentClient is available in chromadb; simplified example:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client

def get_collection(client, name="course_materials"):
    # configure Ollama embedding function
    ollama_url = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/embeddings")
    # choose model name you pulled to ollama, e.g. "all-minilm" or "nomic-embed-text"
    ollama_model = os.environ.get("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    ef = OllamaEmbeddingFunction(model_name=ollama_model, url=ollama_url)
    collection = client.get_or_create_collection(
        name=name,
        metadata={"source": "course_pdfs"},
        embedding_function=ef
    )
    return collection
