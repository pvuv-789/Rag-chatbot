# Common Issues and Solutions

Quick reference for common problems and their solutions.

## Backend Issues

### ❌ ModuleNotFoundError: No module named 'langchain_community'

**Cause**: Using Python 3.13 which doesn't have pre-built wheels for all packages yet.

**Solution**: Use Python 3.11 or 3.12
```bash
cd backend
rmdir /s /q venv
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**See**: [QUICK_FIX.md](QUICK_FIX.md) for detailed steps.

---

### ❌ GEMINI_API_KEY not found

**Cause**: `.env` file not created or API key not set.

**Solution**:
```bash
cd backend
copy .env.example .env
# Edit .env and add your API key
```

Get API key from: https://makersuite.google.com/app/apikey

---

### ❌ Port 8000 already in use

**Solution 1**: Kill the process using port 8000
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

**Solution 2**: Use a different port
```bash
uvicorn main:app --port 8001 --reload
```

---

### ❌ No module named 'utils'

**Cause**: Running from wrong directory.

**Solution**: Make sure you're in the `backend` directory
```bash
cd backend
python -m uvicorn main:app --reload
```

---

### ❌ Virtual environment not activated

**Symptoms**:
- Command not found errors
- Wrong Python version
- Modules not found despite installation

**Solution**:
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Verify - should show (venv) in prompt
```

---

## Frontend Issues

### ❌ Tailwind PostCSS Error

**Error**: `It looks like you're trying to use 'tailwindcss' directly as a PostCSS plugin`

**Cause**: Tailwind v4 installed instead of v3.

**Solution**:
```bash
cd frontend
npm uninstall tailwindcss postcss autoprefixer
npm install -D tailwindcss@3 postcss autoprefixer
npm run dev
```

**See**: [frontend/TROUBLESHOOTING.md](frontend/TROUBLESHOOTING.md) for details.

---

### ❌ Port 5173 in use

**Symptom**: Server starts on 5174 or 5175

**Solution**: This is normal! Vite automatically uses next available port. Just use the URL shown in terminal.

---

### ❌ Cannot find module 'axios'

**Solution**:
```bash
cd frontend
npm install axios
```

---

### ❌ CORS Error

**Error**: `Access to fetch at 'http://localhost:8000' has been blocked by CORS`

**Solution**: Make sure backend is running and check CORS settings in `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    # ... rest of config
)
```

---

### ❌ Blank page in browser

**Check**:
1. Open DevTools (F12) → Console tab
2. Look for error messages
3. Verify backend is running

**Solution**:
```bash
# Clear cache and restart
cd frontend
rm -rf node_modules/.vite
npm run dev
```

---

## Installation Issues

### ❌ Python not found

**Windows**:
- Install from python.org
- Check "Add Python to PATH" during installation

**Linux**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv
```

---

### ❌ npm not found

**Solution**: Install Node.js from https://nodejs.org

Verify:
```bash
node --version  # Should be 18+
npm --version
```

---

### ❌ pip install fails with SSL error

**Solution**:
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

---

## Runtime Issues

### ❌ Google Gemini API Quota Exceeded (429 Error)

**Error**: `429 You exceeded your current quota` or `Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests`

**Cause**: You've hit the free tier limits for Google's embedding API.

**Solution 1 (Recommended)**: Switch to local embeddings (no quota limits):

1. Install sentence-transformers:
```bash
cd backend
venv\Scripts\activate  # Windows
pip install sentence-transformers==2.3.1
```

2. Create or update `.env` file:
```bash
# Add this line to enable local embeddings
USE_LOCAL_EMBEDDINGS=true
```

3. Clear the existing database (it was created with Google embeddings):
```bash
cd backend
rmdir /s /q db  # Windows
# OR
rm -rf db/  # Linux/Mac
```

4. Restart the server:
```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload
```

The first time you upload a PDF, the local model will be downloaded (~80MB). This is a one-time download.

**Solution 2**: Wait 24 hours for the quota to reset, then use sparingly.

**Solution 3**: Upgrade to a paid Google AI plan (not recommended for development).

**Note**: Local embeddings (sentence-transformers) work offline and have no quota limits, making them perfect for development!

---

### ❌ "No documents loaded" error when asking questions

**Cause**: No PDF uploaded yet.

**Solution**: Upload a PDF first using the "Upload PDF" button.

---

### ❌ Slow responses from chatbot

**Possible causes**:
1. Large PDF with many chunks
2. Using gemini-1.5-pro (slower but more accurate)
3. Network latency to Gemini API

**Solutions**:
- Switch to `gemini-1.5-flash` in `.env`
- Reduce chunk size in `loader.py`
- Use smaller PDFs

---

### ❌ ChromaDB errors

**Error**: `Failed to open database` or similar

**Solution**: Delete and recreate database
```bash
cd backend
rm -rf db/
# Restart server - it will recreate
uvicorn main:app --reload
```

---

## Testing Issues

### ❌ API documentation not loading

**Check**: Navigate to http://localhost:8000/docs

**If not working**:
1. Verify backend is running
2. Check terminal for errors
3. Try http://localhost:8000/redoc

---

### ❌ PDF upload fails

**Possible causes**:
1. File too large
2. Not a valid PDF
3. Backend not running

**Solutions**:
- Check file size (keep under 10MB for testing)
- Verify it's a PDF file
- Check backend terminal for errors

---

## Quick Diagnostics

### Backend Health Check
```bash
# Backend must be running first
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","message":"API is running",...}
```

### Frontend Check
```bash
# Should show Tailwind v3
cd frontend
npm list tailwindcss

# Should show no errors
npm run dev
```

### Test Full Stack
1. ✅ Backend running on :8000
2. ✅ Frontend running on :5173
3. ✅ Upload PDF succeeds
4. ✅ Ask question gets response
5. ✅ Sources shown in response

---

## Emergency Reset

If everything is broken, start fresh:

### Backend Reset
```bash
cd backend
rmdir /s /q venv
rmdir /s /q db
rm -rf __pycache__
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Reset
```bash
cd frontend
rm -rf node_modules
rm package-lock.json
npm install
npm run dev
```

---

## Getting More Help

1. **Backend issues**: Check [QUICK_FIX.md](QUICK_FIX.md) and [PYTHON_313_COMPATIBILITY.md](PYTHON_313_COMPATIBILITY.md)
2. **Frontend issues**: Check [frontend/TROUBLESHOOTING.md](frontend/TROUBLESHOOTING.md)
3. **Setup questions**: Check [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
4. **Deployment**: Check [DEPLOYMENT.md](DEPLOYMENT.md)

## Quick Reference Commands

```bash
# Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# Test
curl http://localhost:8000/health
```

---

**Remember**:
- Backend = Python 3.11/3.12 + virtual environment
- Frontend = Node.js 18+ + Tailwind v3
- Both must be running for the app to work
