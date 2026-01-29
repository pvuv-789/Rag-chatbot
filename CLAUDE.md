# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A full-stack RAG (Retrieval-Augmented Generation) chatbot using Google's Gemini API, FastAPI, LangChain, ChromaDB, and React. Users upload PDFs, and the chatbot answers questions based on the document content using vector similarity search and AI-generated responses.

## Development Commands

### Backend (FastAPI + Python)

```bash
# Setup and activate virtual environment (IMPORTANT: Use Python 3.11 or 3.12, NOT 3.13)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run development server (auto-reload enabled)
uvicorn main:app --reload

# Run on custom port
uvicorn main:app --port 8001 --reload

# Production mode
python main.py
```

### Frontend (React + Vite + Tailwind)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm preview

# Lint code
npm run lint
```

### Testing

```bash
# Backend health check
curl http://localhost:8000/health

# Interactive API docs
# Navigate to: http://localhost:8000/docs (Swagger UI)
# Or: http://localhost:8000/redoc (ReDoc)

# Frontend - verify Tailwind version (must be v3, not v4)
cd frontend
npm list tailwindcss
```

## Architecture Overview

### Request Flow

**Document Upload:**
1. User uploads PDF via React UI → POST /load_pdf
2. Backend saves file to `backend/documents/`
3. DocumentLoader (loader.py) extracts text and chunks it
4. VectorStore (vectorstore.py) creates embeddings and stores in ChromaDB
5. Embeddings persist to `backend/db/`

**Question Answering:**
1. User asks question via React UI → POST /ask
2. VectorStore performs similarity search (top 3 chunks)
3. QASystem (qa.py) combines chunks + question into prompt
4. Gemini API generates response
5. Answer + sources returned to frontend

### Module Responsibilities

**Backend (backend/):**
- `main.py` - FastAPI app, all API endpoints, CORS config, component initialization
- `utils/loader.py` - DocumentLoader class: PDF loading, text extraction, chunking with RecursiveCharacterTextSplitter
- `utils/vectorstore.py` - VectorStore class: embedding generation (local or Gemini API), ChromaDB operations, similarity search
- `utils/qa.py` - QASystem class: prompt engineering, Gemini API calls for text generation

**Frontend (frontend/src/):**
- `App.jsx` - Root component, renders ChatBox
- `components/ChatBox.jsx` - Main chat interface, handles API calls, file uploads, message state
- `components/Message.jsx` - Individual message rendering, source citations
- `components/Loader.jsx` - Loading indicator

### Key Technical Details

**Embeddings:**
- By default uses local HuggingFace embeddings (sentence-transformers/all-MiniLM-L6-v2) to avoid API quota limits
- Can switch to Google Gemini API embeddings by setting `USE_LOCAL_EMBEDDINGS=false` in `.env`
- **IMPORTANT:** Cannot mix embedding types - must clear db/ when switching

**Chunking Strategy:**
- Default: 1000 chars with 200 char overlap (configured in main.py:53)
- Uses RecursiveCharacterTextSplitter with separators: "\n\n", "\n", " ", ""

**Vector Database:**
- ChromaDB with persistent storage at `backend/db/`
- Similarity search returns top k=3 chunks (configured in main.py:183)

**CORS Configuration:**
- Allows localhost:5173 and localhost:3000 (common React dev ports)
- Located in main.py:31-37

## Environment Configuration

### Backend (.env in backend/)

Required variables:
```bash
GEMINI_API_KEY=your_api_key_here  # Get from https://makersuite.google.com/app/apikey
CHROMA_DB_PATH=./db
MODEL_NAME=gemini-1.5-flash  # or gemini-1.5-pro (slower, more powerful)
USE_LOCAL_EMBEDDINGS=true  # Recommended: no quota limits
```

### Frontend

API base URL is hardcoded in `frontend/src/components/ChatBox.jsx` - default is `http://localhost:8000`

## Common Issues & Solutions

**Python 3.13 Compatibility:**
- Some packages lack pre-built wheels for Python 3.13
- **Solution:** Use Python 3.11 or 3.12 instead
- See PYTHON_313_COMPATIBILITY.md for detailed fixes

**API Quota Exceeded (429 Error):**
- Hitting Google Gemini API embedding quota
- **Solution:** Set `USE_LOCAL_EMBEDDINGS=true` in backend/.env
- **Must delete backend/db/ folder when switching embedding methods**

**Tailwind v4 PostCSS Error:**
- Frontend requires Tailwind v3, not v4
- **Solution:** `npm uninstall tailwindcss && npm install -D tailwindcss@3`

**Module Not Found Errors:**
- Ensure you're running from correct directory (backend/ for Python commands)
- Ensure virtual environment is activated (`(venv)` in prompt)

**CORS Errors:**
- Verify both backend (port 8000) and frontend (port 5173) are running
- Check allowed origins in main.py:33

## API Endpoints

- `GET /health` - Health check, returns document count
- `POST /load_pdf` - Upload PDF (multipart/form-data)
- `POST /ask` - Ask question (JSON: {question: string})
- `GET /documents` - List uploaded PDFs
- `POST /clear` - Clear vector database

## File Structure Notes

- `backend/documents/` - Created automatically, stores uploaded PDFs
- `backend/db/` - Created automatically, ChromaDB persistent storage
- Frontend uses Vite as build tool (not Create React App)
- Styling via Tailwind CSS utility classes

## Working with This Codebase

**When modifying chunking:**
- Adjust chunk_size and chunk_overlap in main.py:53
- Larger chunks = fewer embeddings but less precise retrieval
- Must clear and re-upload documents after changes

**When modifying prompts:**
- QA prompt template is in qa.py:56-72
- Emphasizes answering only from provided context

**When adding new endpoints:**
- Add to main.py with proper Pydantic models
- Update frontend ChatBox.jsx with corresponding API calls

**When debugging:**
- Backend errors appear in terminal running uvicorn
- Frontend errors in browser console (F12)
- Use /docs endpoint for interactive API testing
