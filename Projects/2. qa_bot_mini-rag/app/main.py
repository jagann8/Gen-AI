import os
from fastapi import FastAPI, UploadFile, File
from app.ingest import ingest_pdf
from app.qa import ask_question

app = FastAPI()

UPLOAD_DIR = "data/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    os.makedirs("data/docs", exist_ok=True) # Ensure this folder exists
    with open(file_path, "wb") as f:
        f.write(await file.read())

    ingest_pdf(file_path)
    return {"message": "Document uploaded and indexed successfully"}

@app.post("/ask")
async def ask(query: str):
    answer = ask_question(query)
    return {"answer": answer}
