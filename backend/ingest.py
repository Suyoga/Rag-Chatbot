# ingest.py
from chroma_client import get_chroma_client, get_collection
from pdf_utils import make_chunks_from_pdf
import argparse
import os
import httpx

def ingest_pdf(pdf_path: str, collection_name="course_materials"):
    client = get_chroma_client()
    timeout = httpx.Timeout(100.0) 
    collection = get_collection(client, name=collection_name)
    source_id = os.path.splitext(os.path.basename(pdf_path))[0]
    items = make_chunks_from_pdf(pdf_path, source_id=source_id)
    texts = [it["text"] for it in items]
    ids = [it["id"] for it in items]
    metadatas = [it["meta"] for it in items]
    # add to chroma; embedding_function will be used to generate vectors
    batch_size = 2
    for i in range(0, len(texts), batch_size):
        collection.add(documents=texts[i:i+batch_size], ids=ids[i:i+batch_size], metadatas=metadatas[i:i+batch_size])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--collection", default="course_materials")
    args = parser.parse_args()
    ingest_pdf(args.pdf, args.collection)
