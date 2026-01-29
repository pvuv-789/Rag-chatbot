# Quick Fix Guide

## Problem: ModuleNotFoundError with Python 3.13

You're seeing this error because Python 3.13 is very new and some packages don't have pre-built wheels yet.

```
ModuleNotFoundError: No module named 'langchain_community'
```

## Fastest Solution (5 minutes)

### Option 1: Use Python 3.11 or 3.12 (Recommended)

1. **Check available Python versions**:
   ```bash
   py --list
   ```

2. **If you have Python 3.11 or 3.12**, use it:
   ```bash
   cd backend

   # Delete old venv
   rmdir /s /q venv

   # Create new venv with Python 3.11
   py -3.11 -m venv venv

   # OR with Python 3.12
   py -3.12 -m venv venv

   # Activate
   venv\Scripts\activate

   # Install
   pip install -r requirements.txt
   ```

3. **If you don't have 3.11/3.12**, download and install:
   - [Python 3.12 Download](https://www.python.org/downloads/)
   - Install it, then repeat step 2

### Option 2: Use the Install Script

We've created an automated script:

```bash
cd backend
install.bat
```

This will:
- Create virtual environment
- Install all dependencies
- Test if everything works
- Show you next steps

### Option 3: Try Force Installing with Python 3.13

```bash
cd backend
venv\Scripts\activate

# Upgrade pip first
python -m pip install --upgrade pip setuptools wheel

# Try installing with no cache
pip install --no-cache-dir -r requirements.txt

# If that fails, install packages one by one
pip install fastapi uvicorn python-dotenv pydantic python-multipart
pip install google-generativeai
pip install pypdf
pip install chromadb
pip install langchain
pip install langchain-community
pip install langchain-google-genai
```

## Verify Installation

After installing, test if everything works:

```bash
cd backend
venv\Scripts\activate
python test_imports.py
```

You should see all green checkmarks ✓

## Start the Backend

Once installation succeeds:

```bash
cd backend
venv\Scripts\activate

# Make sure .env file exists
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start server
uvicorn main:app --reload
```

## Still Having Issues?

### Check Python Version
```bash
python --version
```

Should show 3.11.x or 3.12.x (not 3.13.x)

### Check Virtual Environment
Make sure you see `(venv)` in your terminal prompt after activating.

### Clear Everything and Start Fresh
```bash
cd backend

# Remove virtual environment
rmdir /s /q venv

# Remove pip cache
pip cache purge

# Create new venv (using Python 3.11 or 3.12)
py -3.11 -m venv venv

# Activate
venv\Scripts\activate

# Install
pip install --upgrade pip
pip install -r requirements.txt
```

## Common Errors and Solutions

### Error: "No module named 'langchain_community'"
- **Solution**: Use Python 3.11 or 3.12, not 3.13

### Error: "Microsoft Visual C++ 14.0 is required"
- **Solution**: Install [VS Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or use Python 3.11/3.12 which have pre-built wheels

### Error: "pip is not recognized"
- **Solution**:
  ```bash
  python -m pip install --upgrade pip
  ```

### Error: Virtual environment won't activate
- **Solution**:
  ```bash
  # Try full path
  C:\path\to\backend\venv\Scripts\activate.bat

  # Or use PowerShell
  venv\Scripts\Activate.ps1
  ```

## Summary

**Best solution**: Use Python 3.11 or 3.12

**Quick command**:
```bash
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test_imports.py
```

If all checks pass (✓), you're ready to run:
```bash
uvicorn main:app --reload
```

## Need More Help?

See detailed guide: [PYTHON_313_COMPATIBILITY.md](PYTHON_313_COMPATIBILITY.md)
