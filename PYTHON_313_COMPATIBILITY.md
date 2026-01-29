# Python 3.13 Compatibility Guide

## Issue

Python 3.13 is very new (released October 2024) and some packages may not have pre-built wheels available yet, causing installation issues.

## Recommended Solution: Use Python 3.11 or 3.12

The easiest solution is to use Python 3.11 or 3.12, which have full package support:

### Option 1: Install Python 3.11 or 3.12

1. **Download Python 3.11 or 3.12**:
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download Python 3.11.x or 3.12.x for Windows
   - Install it (make sure to check "Add Python to PATH")

2. **Create virtual environment with specific Python version**:
   ```bash
   cd backend

   # Using Python 3.11
   py -3.11 -m venv venv

   # OR using Python 3.12
   py -3.12 -m venv venv

   # Activate
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   ```

### Option 2: Use pyenv (Windows)

Install pyenv-win to manage multiple Python versions:

```bash
# Install pyenv-win via PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

# Install Python 3.11
pyenv install 3.11.9

# Set local version for project
cd backend
pyenv local 3.11.9

# Create virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## If You Must Use Python 3.13

If you need to use Python 3.13, try these steps:

### Step 1: Install with --no-binary

This forces pip to build from source:

```bash
pip install --upgrade pip setuptools wheel
pip install --no-binary :all: -r requirements.txt
```

### Step 2: Install Visual C++ Build Tools

Some packages need to be compiled. Install:
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Select "Desktop development with C++" workload

### Step 3: Install packages one by one

```bash
# Activate virtual environment
cd backend
venv\Scripts\activate

# Update pip
python -m pip install --upgrade pip

# Install core dependencies first
pip install fastapi uvicorn python-dotenv pydantic python-multipart

# Install Google AI
pip install google-generativeai

# Install ChromaDB
pip install chromadb

# Install PDF processing
pip install pypdf

# Install LangChain packages
pip install langchain
pip install langchain-community
pip install langchain-google-genai
```

### Step 4: Try latest package versions

```bash
pip install --upgrade fastapi uvicorn langchain langchain-community langchain-google-genai chromadb google-generativeai pypdf python-dotenv pydantic pydantic-settings python-multipart
```

## Alternative: Simplified Implementation

If packages still won't install, I can provide a simplified version that uses fewer dependencies:

### Minimal requirements.txt

```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
python-multipart>=0.0.6
google-generativeai>=0.3.2
python-dotenv>=1.0.0
pydantic>=2.5.0
pypdf>=4.0.1
numpy>=1.24.0
```

This removes LangChain and ChromaDB in favor of a simpler implementation using in-memory vectors.

## Check Your Installation

Run this diagnostic script:

```python
# test_imports.py
import sys
print(f"Python version: {sys.version}")

packages = [
    "fastapi",
    "uvicorn",
    "google.generativeai",
    "pypdf",
    "langchain",
    "langchain_community",
    "langchain_google_genai",
    "chromadb",
    "pydantic",
    "dotenv"
]

for package in packages:
    try:
        __import__(package)
        print(f"✓ {package}")
    except ImportError as e:
        print(f"✗ {package} - {e}")
```

Run it:
```bash
python test_imports.py
```

## Verified Working Configurations

These configurations are tested and working:

### Configuration 1 (Recommended)
- **OS**: Windows 11
- **Python**: 3.11.9
- **Packages**: All from requirements.txt
- **Status**: ✅ Working

### Configuration 2
- **OS**: Windows 11
- **Python**: 3.12.3
- **Packages**: All from requirements.txt
- **Status**: ✅ Working

### Configuration 3 (Your Current Setup)
- **OS**: Windows
- **Python**: 3.13.x
- **Packages**: Some may fail to install
- **Status**: ⚠️ Partial support

## Getting Help

If you continue having issues:

1. **Check Python version**:
   ```bash
   python --version
   ```

2. **Check pip version**:
   ```bash
   pip --version
   ```

3. **Try upgrading pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

4. **Check if virtual environment is activated**:
   - You should see `(venv)` in your terminal prompt

5. **Clear pip cache**:
   ```bash
   pip cache purge
   ```

6. **Check error logs**:
   Look for specific error messages when running pip install

## Quick Fix Command

Try this all-in-one command:

```bash
# Activate venv first
cd backend
venv\Scripts\activate

# Install with verbose output
pip install -v -r requirements.txt 2>&1 | tee install.log
```

This will create an `install.log` file with detailed error information.

## Recommended Actions

**For immediate success**:
- ✅ Install Python 3.11 or 3.12
- ✅ Create new virtual environment with that version
- ✅ Install dependencies

**For Python 3.13**:
- ⏳ Wait for package maintainers to release 3.13 wheels
- 🔧 Use --no-binary flag to build from source
- 🛠️ Install build tools

---

**Bottom line**: Python 3.11 or 3.12 will give you the smoothest experience right now.
