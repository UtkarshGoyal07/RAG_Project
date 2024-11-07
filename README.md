# **RAG FastAPI Server**

This project is a lightweight **FastAPI** server for **Retrieval-Augmented Generation (RAG)** that allows for document ingestion and querying. It utilizes **ChromaDB** for storing embeddings and document content, and **sentence-transformers/all-MiniLM-L6-v2** from Hugging Face for creating embeddings. The server supports non-blocking API endpoints and efficient concurrency handling.

## **Features**
- **Ingest Documents**: Supports PDF, DOCX, and TXT file formats.
- **Query Documents**: Allows querying of ingested documents based on text similarity.
- **Persistent Storage**: Uses ChromaDB for persistent storage of documents and embeddings.
- **Health Check Endpoint**: Check if the API is running properly.

## **Tech Stack**
- **FastAPI**: Web framework for building APIs.
- **ChromaDB**: Database for embedding storage and retrieval.
- **Sentence Transformers**: Hugging Face model (`all-MiniLM-L6-v2`) for embedding generation.
- **Uvicorn**: ASGI server for running the FastAPI app.

## **Requirements**

Before you begin, ensure you have the following installed:
- **Python 3.8** or later
- **Git**

## **Installation**

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/RAG_FastAPI_Project.git
   cd RAG_FastAPI_Project
   py -m venv env                 # Create a virtual environment
   env\Scripts\activate.bat       # Activate the environment on Windows
   py -m pip install -r requirements.txt   # Install required packages

   py main.py
