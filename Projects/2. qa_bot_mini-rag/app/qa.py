import os
import faiss
import pickle
import numpy as np
from google import genai
from google.genai import types # Added this import
from sentence_transformers import SentenceTransformer
from app.prompt import QA_PROMPT
from dotenv import load_dotenv

load_dotenv()

# CHANGE 1: Explicitly set the API version to 'v1'
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={'api_version': 'v1'} 
)

##
#
# # Replace with your actual API key setup
# client = genai.Client(api_key="AIzaSyBs2vfn-fQEEiKPUhg9unzH7GSFwuX7XMw")

# print("Listing available models...")
# for model in client.models.list():
#     # This will print the exact strings you are allowed to use
#     print(model.name)
# 
# #
model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "data/faiss_index/index.faiss"
META_PATH = "data/faiss_index/meta.pkl"

def ask_question(question: str):
    if not os.path.exists(INDEX_PATH):
        return "Error: Index file not found. Please upload a document first."

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        chunks = pickle.load(f)

    query_embedding = model.encode([question]).astype("float32")
    distances, indices = index.search(query_embedding, k=4)

    context = "\n\n".join([chunks[i] for i in indices[0] if i < len(chunks)])

    prompt = QA_PROMPT.format(
        context=context,
        question=question
    )

    # CHANGE 2: Ensure we are using the stable model string
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text
