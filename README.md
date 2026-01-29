# RAG Chatbot with Gemini API

A full-stack AI chatbot system using Retrieval-Augmented Generation (RAG) with Google's Gemini API, FastAPI, LangChain, ChromaDB, and React.

## Overview

This chatbot can answer questions based on PDF documents you upload. It uses:
- **RAG (Retrieval-Augmented Generation)**: Retrieves relevant information from documents before generating responses
- **Gemini AI**: Google's powerful language model for intelligent responses
- **Vector Search**: ChromaDB for fast similarity search
- **Modern UI**: React + Tailwind CSS for a beautiful chat interface

## Architecture

```
User → Chat UI (React)
         ↓
Backend (FastAPI)
         ↓
Search Vector DB (ChromaDB)
         ↓
Found relevant info (top 3 docs)
         ↓
Combine info + user query → Gemini AI
         ↓
Send answer → Frontend
```

## Features

- Upload PDF documents and create searchable knowledge base
- Ask questions and get AI-generated answers based on your documents
- View source citations for transparency
- Real-time chat interface with typing indicators
- Responsive design for mobile and desktop
- Fast vector similarity search with ChromaDB
- Persistent storage of document embeddings

## Project Structure

```
rag-chatbot/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── utils/
│   │   ├── loader.py        # PDF processing
│   │   ├── vectorstore.py   # ChromaDB operations
│   │   └── qa.py            # Question answering logic
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment template
│   ├── db/                  # ChromaDB storage (created automatically)
│   └── documents/           # Uploaded PDFs (created automatically)
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatBox.jsx  # Main chat interface
    │   │   ├── Message.jsx  # Message component
    │   │   └── Loader.jsx   # Loading indicator
    │   ├── App.jsx          # Root component
    │   └── index.css        # Tailwind styles
    ├── package.json
    └── vite.config.js
```

## Prerequisites

- **Python 3.11 or 3.12** (recommended - see note below)
- Node.js 18 or higher
- npm or yarn
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

> **⚠️ Python 3.13 Note**: If you're using Python 3.13, some packages may not have pre-built wheels yet. See [PYTHON_313_COMPATIBILITY.md](PYTHON_313_COMPATIBILITY.md) for solutions. We recommend using Python 3.11 or 3.12 for the best experience.

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from the example:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

5. Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
CHROMA_DB_PATH=./db
MODEL_NAME=gemini-1.5-flash
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Create `.env` file if you need to change the API URL:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

## Running the Application

### Start the Backend

1. Make sure you're in the backend directory with the virtual environment activated
2. Run the FastAPI server:

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
python main.py
```

The backend will start at `http://localhost:8000`

### Start the Frontend

1. In a new terminal, navigate to the frontend directory
2. Run the development server:

```bash
npm run dev
```

The frontend will start at `http://localhost:5173`

## Usage

1. **Upload a PDF**: Click the "Upload PDF" button in the top-right corner
2. **Wait for Processing**: The system will process and store the document
3. **Ask Questions**: Type your question in the chat box and press Enter
4. **View Answers**: The AI will respond with answers based on your documents
5. **Check Sources**: Expand the "Sources" section to see which document chunks were used

## API Endpoints

### Health Check
```http
GET /health
```
Returns the API status and document count.

### Upload PDF
```http
POST /load_pdf
Content-Type: multipart/form-data

file: <PDF file>
```

### Ask Question
```http
POST /ask
Content-Type: application/json

{
  "question": "What is this document about?"
}
```

### List Documents
```http
GET /documents
```

### Clear Database
```http
POST /clear
```

## Configuration

### Backend Configuration (`.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | (required) |
| `CHROMA_DB_PATH` | Path to store vector database | `./db` |
| `MODEL_NAME` | Gemini model to use | `gemini-1.5-flash` |

**Available Models:**
- `gemini-1.5-flash` - Faster, lower cost
- `gemini-1.5-pro` - More powerful, higher quality

### Frontend Configuration

You can modify the API base URL in `src/components/ChatBox.jsx`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Troubleshooting

### Backend Issues

**Error: GEMINI_API_KEY not found**
- Make sure you created the `.env` file in the backend directory
- Verify the API key is correct and has no extra spaces

**Error: Module not found**
- Ensure you activated the virtual environment
- Run `pip install -r requirements.txt` again

**ChromaDB errors**
- Delete the `db/` folder and restart the server
- Make sure you have write permissions in the backend directory

### Frontend Issues

**Cannot connect to backend**
- Verify the backend is running on `http://localhost:8000`
- Check CORS settings in `main.py` if using a different port
- Make sure both servers are running

**Tailwind styles not working**
- Run `npm install` again
- Delete `node_modules` and reinstall

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **Frontend**: Create new components in `src/components/`
3. **Utilities**: Add helper functions in `backend/utils/`

### Testing the API

Use the interactive API docs at `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).

### Building for Production

**Backend:**
```bash
# Use a production ASGI server
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
npm run build
# Serve the dist/ folder with nginx or another web server
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: Framework for LLM applications
- **ChromaDB**: Vector database for embeddings
- **Google Generative AI**: Gemini API for embeddings and responses
- **PyPDF**: PDF text extraction
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API calls

## Security Considerations

- Never commit `.env` files with real API keys
- Use environment variables for all sensitive data
- Add rate limiting for production deployments
- Validate and sanitize all file uploads
- Use HTTPS in production

## Performance Tips

1. **Chunking**: Adjust `chunk_size` in `DocumentLoader` for optimal performance
2. **Top K**: Change `k=3` in similarity search for more/fewer sources
3. **Model Selection**: Use `gemini-1.5-flash` for faster responses
4. **Caching**: Consider implementing response caching for common questions

## License

This project is provided as-is for educational purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the [API documentation](http://localhost:8000/docs) when the server is running
- Open an issue on GitHub

## Acknowledgments

- Google for the Gemini API
- LangChain community
- FastAPI framework
- React and Vite teams

---

**Built with ❤️ using modern AI and web technologies**
