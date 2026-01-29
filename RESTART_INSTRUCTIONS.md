# How to Restart the Application

The fixes have been applied to both backend and frontend. Follow these steps to restart and test:

## Backend Restart

1. **Stop the current backend server** (if running):
   - Press `Ctrl+C` in the terminal where backend is running

2. **Restart the backend** (IMPORTANT - use the correct command):

   **Option 1 - Use the startup script (Recommended):**
   ```bash
   cd backend
   start.bat  # Windows
   # OR
   ./start.sh  # Linux/Mac
   ```

   **Option 2 - Manual start:**
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # OR
   source venv/bin/activate  # Linux/Mac

   # IMPORTANT: Must specify --host 0.0.0.0 to bind to all interfaces
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Verify backend is running**:
   - Open browser: http://localhost:8000/docs
   - You should see "FastAPI" documentation page

## Frontend Restart

1. **Stop the current frontend server** (if running):
   - Press `Ctrl+C` in the terminal where frontend is running

2. **Restart the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open the application**:
   - The terminal will show the URL (usually http://localhost:5173)
   - Open that URL in your browser

## What Was Fixed

### Backend Changes:
1. ✅ **Fixed CORS to allow all origins in development** (allow_origins=["*"])
2. ✅ **Created start.bat/start.sh scripts** that properly bind to 0.0.0.0
3. ✅ Added `USE_LOCAL_EMBEDDINGS=true` to .env (avoids API quota issues)
4. ✅ Enhanced error logging with detailed console output
5. ✅ Improved file upload handling with better validation
6. ✅ Better error messages for debugging

**CRITICAL:** You must start uvicorn with `--host 0.0.0.0` or the frontend can't connect!

### Frontend Changes:
1. ✅ Removed explicit `Content-Type` header (axios sets it automatically for FormData)
2. ✅ Added detailed console logging for debugging
3. ✅ Better error messages showing actual backend errors
4. ✅ Case-insensitive PDF file validation

## Testing the Fixes

After restarting both servers:

1. **Test File Upload**:
   - Click "Upload PDF" button
   - Select a PDF file
   - Watch browser console (F12 → Console tab) for logs
   - Watch backend terminal for upload logs
   - Should see success message in chat

2. **Test Question Asking**:
   - Type a question in the text box
   - Press Enter or click Send
   - Watch browser console for logs
   - Watch backend terminal for processing logs
   - Should see answer with sources

## Troubleshooting

### If upload still fails:
1. Open browser console (F12)
2. Look for the error message
3. Check backend terminal for detailed logs
4. Verify backend is running: `curl http://localhost:8000/health`

### If question asking fails:
1. Make sure you uploaded a PDF first
2. Check browser console for errors
3. Check backend terminal for logs
4. Verify documents loaded: `curl http://localhost:8000/documents`

### Common Issues:
- **CORS error**: Make sure backend was restarted after the changes
- **Connection refused**: Backend not running on port 8000
- **No documents loaded**: Upload a PDF first before asking questions
- **Port already in use**: Kill the process or use a different port

## Viewing Logs

**Backend logs** appear in the terminal where you ran `uvicorn main:app --reload`

**Frontend logs** appear in:
- Browser console (F12 → Console tab)
- Terminal where you ran `npm run dev` (for build errors)

## Quick Test Command

```bash
# Test backend health
curl http://localhost:8000/health

# Test backend ask endpoint (should return an answer if docs are loaded)
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"question\":\"test\"}"
```

Now the application should work without the upload and 400 errors!
