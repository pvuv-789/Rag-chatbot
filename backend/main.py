"""
Main FastAPI Application
Handles API endpoints for PDF upload and question answering
Compatible with Python 3.11+
"""

from __future__ import annotations
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from dotenv import load_dotenv

from utils.loader import DocumentLoader
from utils.vectorstore import VectorStore
from utils.qa import QASystem

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="AI Chatbot using Retrieval-Augmented Generation with Gemini API",
    version="1.0.0"
)

# CORS configuration - Allow all localhost/127.0.0.1 for development
# For production, restrict this to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./db")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
DOCUMENTS_DIR = "./documents"

# Validate API key
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Create documents directory
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

# Initialize components
document_loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)
# Use local embeddings by default to avoid API quota limits
# Set use_local_embeddings=False in .env to use Google API embeddings
USE_LOCAL_EMBEDDINGS = os.getenv("USE_LOCAL_EMBEDDINGS", "true").lower() == "true"
vector_store = VectorStore(
    api_key=GEMINI_API_KEY,
    persist_directory=CHROMA_DB_PATH,
    use_local_embeddings=USE_LOCAL_EMBEDDINGS
)
qa_system = QASystem(api_key=GEMINI_API_KEY, model_name=MODEL_NAME)


# Pydantic models
class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    num_sources: int


class LoadPDFResponse(BaseModel):
    status: str
    message: str
    chunks_stored: int


class HealthResponse(BaseModel):
    status: str
    message: str
    model: str
    documents_count: int


# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "load_pdf": "/load_pdf",
            "ask": "/ask",
            "clear": "/clear"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        doc_count = vector_store.get_collection_count()
        return HealthResponse(
            status="healthy",
            message="API is running",
            model=MODEL_NAME,
            documents_count=doc_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/load_pdf", response_model=LoadPDFResponse)
async def load_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file

    Args:
        file: PDF file to upload

    Returns:
        Status message and number of chunks stored
    """
    try:
        # Log the upload attempt
        print(f"Received file upload request: {file.filename}")

        # Validate file exists
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="Invalid file: no filename")

        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Save uploaded file
        file_path = os.path.join(DOCUMENTS_DIR, file.filename)
        print(f"Saving file to: {file_path}")

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        print(f"File saved successfully, size: {os.path.getsize(file_path)} bytes")

        # Load and process PDF
        print("Processing PDF...")
        chunks = document_loader.load_pdf(file_path)
        print(f"PDF split into {len(chunks)} chunks")

        # Add to vector store
        print("Adding to vector store...")
        num_chunks = vector_store.add_documents(chunks)
        print(f"Successfully stored {num_chunks} chunks")

        return LoadPDFResponse(
            status="success",
            message=f"PDF '{file.filename}' processed and stored successfully",
            chunks_stored=num_chunks
        )

    except HTTPException as he:
        print(f"HTTP Exception: {he.detail}")
        raise he
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an AI-generated answer

    Args:
        request: Question request containing the user's question

    Returns:
        Answer with source documents
    """
    try:
        # Log the question
        print(f"Received question: {request.question}")

        # Validate question
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")

        # Check if vector store has documents
        doc_count = vector_store.get_collection_count()
        print(f"Vector store has {doc_count} documents")

        if doc_count == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents loaded. Please upload a PDF first using /load_pdf"
            )

        # Search for relevant documents
        print("Searching for relevant documents...")
        relevant_docs = vector_store.similarity_search(request.question, k=3)
        print(f"Found {len(relevant_docs)} relevant documents")

        # Generate answer
        print("Generating answer...")
        result = qa_system.generate_answer(request.question, relevant_docs)
        print("Answer generated successfully")

        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            num_sources=result["num_sources"]
        )

    except HTTPException as he:
        print(f"HTTP Exception in ask: {he.detail}")
        raise he
    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


@app.post("/clear")
async def clear_database():
    """
    Clear all documents from the vector database

    Returns:
        Status message
    """
    try:
        vector_store.clear_database()
        return {
            "status": "success",
            "message": "Vector database cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing database: {str(e)}")


@app.get("/documents")
async def list_documents():
    """
    List all uploaded PDF documents

    Returns:
        List of document filenames
    """
    try:
        files = [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith('.pdf')]
        return {
            "status": "success",
            "documents": files,
            "count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
