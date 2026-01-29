@echo off
echo Starting RAG Chatbot Backend...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Start uvicorn with proper host binding
echo Backend will be available at:
echo   - http://localhost:8000
echo   - http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
