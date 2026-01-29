# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
│                      (React + Tailwind CSS)                      │
│                     http://localhost:5173                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             │ (axios requests)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FASTAPI BACKEND                            │
│                     http://localhost:8000                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Endpoints:                                           │  │
│  │  • POST /load_pdf  - Upload & process PDFs               │  │
│  │  • POST /ask       - Ask questions                       │  │
│  │  • GET  /health    - Health check                        │  │
│  │  • GET  /documents - List uploaded files                 │  │
│  │  • POST /clear     - Clear database                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │         PROCESSING LAYER                │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │   DocumentLoader (loader.py)     │  │
        │  │   • Load PDFs                    │  │
        │  │   • Extract text                 │  │
        │  │   • Split into chunks            │  │
        │  └──────────────────────────────────┘  │
        │               │                         │
        │               ▼                         │
        │  ┌──────────────────────────────────┐  │
        │  │   VectorStore (vectorstore.py)   │  │
        │  │   • Create embeddings            │  │
        │  │   • Store in ChromaDB            │  │
        │  │   • Similarity search            │  │
        │  └──────────────────────────────────┘  │
        │               │                         │
        │               ▼                         │
        │  ┌──────────────────────────────────┐  │
        │  │      QASystem (qa.py)            │  │
        │  │   • Combine context + query      │  │
        │  │   • Generate response            │  │
        │  │   • Return with sources          │  │
        │  └──────────────────────────────────┘  │
        └────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────┐
        │         EXTERNAL SERVICES               │
        │                                         │
        │  ┌──────────────────────────────────┐  │
        │  │     ChromaDB (Local Storage)     │  │
        │  │     • Vector embeddings          │  │
        │  │     • Fast similarity search     │  │
        │  │     • Persistent storage          │  │
        │  └──────────────────────────────────┘  │
        │               │                         │
        │               ▼                         │
        │  ┌──────────────────────────────────┐  │
        │  │   Google Gemini API              │  │
        │  │   • Embedding generation         │  │
        │  │   • Text generation              │  │
        │  │   • Natural language processing   │  │
        │  └──────────────────────────────────┘  │
        └────────────────────────────────────────┘
```

## Data Flow

### 1. Document Upload Flow

```
User uploads PDF
       │
       ▼
Frontend sends to /load_pdf
       │
       ▼
Backend receives file
       │
       ▼
DocumentLoader processes PDF
   • Extracts text from pages
   • Splits into chunks (1000 chars)
   • Adds metadata
       │
       ▼
VectorStore creates embeddings
   • Calls Gemini embedding API
   • Generates vector representations
       │
       ▼
Store in ChromaDB
   • Persist vectors to disk
   • Index for fast search
       │
       ▼
Return success to frontend
```

### 2. Question Answering Flow

```
User types question
       │
       ▼
Frontend sends to /ask
       │
       ▼
Backend receives question
       │
       ▼
VectorStore searches for relevant chunks
   • Convert question to embedding
   • Similarity search in ChromaDB
   • Return top 3 most relevant chunks
       │
       ▼
QASystem generates answer
   • Combine chunks into context
   • Create prompt with question
   • Call Gemini API for response
       │
       ▼
Return answer + sources to frontend
       │
       ▼
Display in chat UI
```

## Component Breakdown

### Frontend Components

```
App.jsx
  └── ChatBox.jsx
       ├── Message.jsx (for each message)
       │    └── Sources (collapsible)
       └── Loader.jsx (when waiting)
```

### Backend Modules

```
main.py (FastAPI app)
  │
  ├── utils/loader.py
  │    └── DocumentLoader class
  │         ├── load_pdf()
  │         └── load_multiple_pdfs()
  │
  ├── utils/vectorstore.py
  │    └── VectorStore class
  │         ├── add_documents()
  │         ├── similarity_search()
  │         └── clear_database()
  │
  └── utils/qa.py
       └── QASystem class
            ├── create_prompt()
            └── generate_answer()
```

## Technology Stack Details

### Backend Technologies

| Technology | Purpose | Version |
|-----------|---------|---------|
| FastAPI | Web framework | 0.109+ |
| Uvicorn | ASGI server | 0.27+ |
| LangChain | LLM framework | 0.1+ |
| ChromaDB | Vector database | 0.4+ |
| PyPDF | PDF processing | 4.0+ |
| Google GenAI | Gemini API | 0.3+ |
| python-dotenv | Environment vars | 1.0+ |

### Frontend Technologies

| Technology | Purpose | Version |
|-----------|---------|---------|
| React | UI library | 18+ |
| Vite | Build tool | 5+ |
| Tailwind CSS | Styling | 3+ |
| Axios | HTTP client | 1+ |

## Security Architecture

```
┌──────────────────────────────────────┐
│         Security Layers              │
├──────────────────────────────────────┤
│  1. API Key Protection               │
│     • Stored in .env (not in git)    │
│     • Never exposed to frontend      │
│                                      │
│  2. CORS Configuration               │
│     • Specific origin allowlist      │
│     • localhost only in dev          │
│                                      │
│  3. Input Validation                 │
│     • PDF file type check            │
│     • Question length limits         │
│     • Pydantic models                │
│                                      │
│  4. File Upload Security             │
│     • File type validation           │
│     • Size limits                    │
│     • Secure file storage            │
└──────────────────────────────────────┘
```

## Deployment Architecture (Production)

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
┌─────────────────┐            ┌─────────────────┐
│   Frontend      │            │   Frontend      │
│   (Nginx/CDN)   │            │   (Nginx/CDN)   │
└────────┬────────┘            └────────┬────────┘
         │                              │
         └──────────────┬───────────────┘
                        ▼
              ┌──────────────────┐
              │  API Gateway     │
              └────────┬─────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
┌─────────────────┐        ┌─────────────────┐
│   Backend API   │        │   Backend API   │
│   (Gunicorn)    │        │   (Gunicorn)    │
└────────┬────────┘        └────────┬────────┘
         │                          │
         └──────────┬───────────────┘
                    ▼
         ┌────────────────────┐
         │   ChromaDB         │
         │   (Persistent)     │
         └────────────────────┘
                    │
                    ▼
         ┌────────────────────┐
         │   Gemini API       │
         │   (Google Cloud)   │
         └────────────────────┘
```

## Performance Considerations

### Bottlenecks and Solutions

1. **PDF Processing**
   - Bottleneck: Large PDFs take time to process
   - Solution: Async processing, progress indicators

2. **Embedding Generation**
   - Bottleneck: API rate limits
   - Solution: Batch processing, caching

3. **Vector Search**
   - Bottleneck: Large vector databases
   - Solution: Indexing, limiting search results

4. **Response Generation**
   - Bottleneck: Gemini API latency
   - Solution: Use flash model, implement streaming

## Scalability

### Horizontal Scaling

- Multiple backend instances behind load balancer
- Shared ChromaDB (persistent volume)
- Stateless API design

### Vertical Scaling

- Increase chunk size for fewer embeddings
- Optimize vector dimensions
- Use faster embedding models

## Monitoring Points

```
Frontend:
  • User interaction events
  • API call success/failure rates
  • Page load times

Backend:
  • Request/response times
  • Error rates
  • Vector database query times
  • PDF processing times

External:
  • Gemini API latency
  • API quota usage
  • ChromaDB performance
```

---

This architecture provides a solid foundation for a production-ready RAG system that can scale with your needs.
