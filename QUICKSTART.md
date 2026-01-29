# Quick Start Guide

Get your RAG Chatbot up and running in 5 minutes!

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

## Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env    # Windows
cp .env.example .env      # Mac/Linux

# Edit .env and add your API key
# GEMINI_API_KEY=your_api_key_here
```

## Step 3: Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install
```

## Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
# Make sure venv is activated
uvicorn main:app --reload
```
Backend will run at: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend will run at: http://localhost:5173

## Step 5: Use the Chatbot

1. Open http://localhost:5173 in your browser
2. Click "Upload PDF" button
3. Select a PDF file from your computer
4. Wait for processing (you'll see a success message)
5. Ask questions about your document!

## Example Questions

After uploading a PDF, try asking:
- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"
- "Tell me about [specific topic from your document]"

## Common Issues

**Backend won't start:**
- Check if port 8000 is already in use
- Verify your GEMINI_API_KEY is set in .env
- Make sure virtual environment is activated

**Frontend won't start:**
- Check if port 5173 is already in use
- Try deleting node_modules and running `npm install` again

**Can't upload PDF:**
- Make sure backend is running
- Check browser console for errors
- Verify the file is a valid PDF

**No response from chatbot:**
- Make sure you uploaded a PDF first
- Check backend terminal for error messages
- Verify your API key is valid

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the API docs at http://localhost:8000/docs
- Customize the UI in `frontend/src/components/`
- Add more features to the backend in `backend/main.py`

Happy chatting! 🚀
