main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import fitz  
from docx import Document
from typing import List
import os
import uvicorn
from tempfile import NamedTemporaryFile

app = FastAPI()

CHROMA_DB_PATH = "./chromadb_storage"
chromadb_client = PersistentClient(path=CHROMA_DB_PATH)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def extract_text_from_pdf(file_content: bytes) -> str:
    text = ""
    try:
        doc = fitz.open(stream=file_content, filetype="pdf")
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error while extracting text from PDF: {e}")
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    text = ""
    try:
        with open("temp.docx", "wb") as f:
            f.write(file_content)
        doc = Document("temp.docx")
        for para in doc.paragraphs:
            text += para.text + "\n"
        os.remove("temp.docx")
    except Exception as e:
        print(f"Error while extracting text from DOCX: {e}")
    return text

def extract_text(file_content: bytes, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_content)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_content)
    elif filename.endswith(".txt"):
        return file_content.decode("utf-8")
    else:
        raise ValueError("Unsupported file format")

app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}")  # Log file name
        content = await file.read()
        text = extract_text(content, file.filename)
        print(f"Extracted text: {text[:100]}")  # Print the first 100 characters for debugging

        # Generate embedding
        embedding = model.encode(text)
        print(f"Generated embedding: {embedding[:10]}")  # Print first 10 embedding values

        # Store in ChromaDB
        chromadb_client.store_document(content=text, embedding=embedding)
        return JSONResponse(content={"message": "Document ingested successfully"}, status_code=201)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Error occurred during ingestion: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during ingestion")

@app.get("/query")
async def query_documents(user_query: str):
    try:
        query_embedding = model.encode(user_query)
        
        results = chromadb_client.query(query_embedding)
        
        return JSONResponse(content={"results": results}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during querying")


@app.get("/check-health")
async def test_endpoint():
    return {"message": "API Healthy!"}


if _name_ == "_main_":
    uvicorn.run("main:app", reload=True)
    
