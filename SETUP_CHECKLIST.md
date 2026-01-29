# Setup Checklist

Use this checklist to ensure your RAG Chatbot is properly configured.

## Prerequisites
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Git installed (optional, for version control)

## Backend Setup
- [ ] Created virtual environment (`python -m venv venv`)
- [ ] Activated virtual environment
- [ ] Installed Python dependencies (`pip install -r requirements.txt`)
- [ ] Created `.env` file from `.env.example`
- [ ] Added Gemini API key to `.env`
- [ ] Verified `CHROMA_DB_PATH` in `.env` (default: `./db`)
- [ ] Verified `MODEL_NAME` in `.env` (default: `gemini-1.5-flash`)

## Frontend Setup
- [ ] Installed Node dependencies (`npm install`)
- [ ] Verified Tailwind CSS is installed
- [ ] (Optional) Created `.env` file if custom API URL needed

## Testing
- [ ] Backend starts without errors (`uvicorn main:app --reload`)
- [ ] Backend is accessible at http://localhost:8000
- [ ] API docs load at http://localhost:8000/docs
- [ ] Health check endpoint returns success
- [ ] Frontend starts without errors (`npm run dev`)
- [ ] Frontend is accessible at http://localhost:5173
- [ ] No console errors in browser

## First Use
- [ ] Upload a test PDF document
- [ ] Wait for success message
- [ ] Ask a test question
- [ ] Receive AI response with sources
- [ ] Verify sources are relevant

## Optional Enhancements
- [ ] Customize UI colors in Tailwind config
- [ ] Add more PDF documents
- [ ] Test with different question types
- [ ] Try both Gemini models (flash vs pro)
- [ ] Adjust chunk size for better retrieval
- [ ] Enable CORS for production domains
- [ ] Set up production deployment

## Troubleshooting
If you encounter issues:

1. **Backend Issues:**
   - Check virtual environment is activated
   - Verify `.env` file exists and has correct API key
   - Check terminal for error messages
   - Try deleting `db/` folder and restarting

2. **Frontend Issues:**
   - Clear browser cache
   - Check browser console for errors
   - Verify backend is running
   - Try deleting `node_modules` and reinstalling

3. **API Issues:**
   - Verify Gemini API key is valid
   - Check API quota/limits
   - Test with simpler questions first
   - Review API docs at http://localhost:8000/docs

## Environment Variables Summary

**Backend (.env):**
```
GEMINI_API_KEY=your_key_here
CHROMA_DB_PATH=./db
MODEL_NAME=gemini-1.5-flash
```

**Frontend (.env) - Optional:**
```
VITE_API_BASE_URL=http://localhost:8000
```

## Port Configuration

Default ports:
- Backend: 8000
- Frontend: 5173

To change ports:
- Backend: `uvicorn main:app --port 8001`
- Frontend: Modify `vite.config.js`

## Next Steps After Setup

1. Read the full [README.md](README.md)
2. Try the [QUICKSTART.md](QUICKSTART.md) guide
3. Explore the API documentation
4. Customize the UI components
5. Add error handling
6. Implement authentication (if needed)
7. Deploy to production

---

✅ **Setup Complete!** Start building amazing RAG applications!
