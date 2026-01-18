import os
import pickle
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/docs"
INDEX_PATH = "data/faiss_index/index.faiss"
META_PATH = "data/faiss_index/meta.pkl"

os.makedirs("data/faiss_index", exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_pdf(file_path: str):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Chunking
    chunk_size = 800
    overlap = 150

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            metadata = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(embeddings.shape[1])
        metadata = []

    index.add(embeddings)
    metadata.extend(chunks)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)
