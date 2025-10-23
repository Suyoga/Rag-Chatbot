import fitz  
import re
from typing import List, Dict

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    texts = []
    for page in doc:
        text = page.get_text("text")
        # naive clean: remove repeated white-space
        text = re.sub(r'\n{2,}', '\n\n', text)
        texts.append(text)
    return "\n\n".join(texts)

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Chunk by characters with overlap. This is simple and robust when tokenizers aren't available.
    chunk_size and overlap are in characters; you can adjust to tokens with tiktoken if you want.
    """
    texts = []
    start = 0
    length = len(text)
    while start < length:
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            texts.append(chunk)
        start += chunk_size - overlap
    return texts

def make_chunks_from_pdf(path: str, source_id: str, chunk_size=1200, overlap=256):
    text = extract_text_from_pdf(path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    items = []
    for i, chunk in enumerate(chunks):
        items.append({
            "id": f"{source_id}_chunk_{i}",
            "text": chunk,
            "meta": {
                "source": path,
                "chunk_index": i
            }
        })
    return items
