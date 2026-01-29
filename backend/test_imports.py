"""
Diagnostic script to test if all required packages are installed
Compatible with Python 3.11+
"""

from __future__ import annotations
import sys
import io

print("=" * 60)
print("RAG Chatbot - Package Installation Test")
print("=" * 60)
print(f"\nPython version: {sys.version}")
print(f"Python executable: {sys.executable}")
print("\n" + "=" * 60)
print("Testing package imports...")
print("=" * 60 + "\n")

packages = [
    ("fastapi", "FastAPI web framework"),
    ("uvicorn", "ASGI server"),
    ("google.generativeai", "Google Gemini API"),
    ("pypdf", "PDF processing"),
    ("langchain", "LangChain framework"),
    ("langchain_community", "LangChain community modules"),
    ("langchain_google_genai", "LangChain Google integration"),
    ("chromadb", "Vector database"),
    ("pydantic", "Data validation"),
    ("dotenv", "Environment variables"),
    ("multipart", "Multipart form data"),
]

success_count = 0
failed_packages = []

for package, description in packages:
    try:
        module = __import__(package)
        version = getattr(module, "__version__", "unknown")
        print(f"[OK] {package:25} v{version:15} - {description}")
        success_count += 1
    except ImportError as e:
        print(f"[FAIL] {package:25} {'FAILED':15} - {description}")
        print(f"       Error: {e}")
        failed_packages.append(package)

print("\n" + "=" * 60)
print(f"Results: {success_count}/{len(packages)} packages imported successfully")
print("=" * 60)

if failed_packages:
    print("\n[X] Failed packages:")
    for pkg in failed_packages:
        print(f"   - {pkg}")

    print("\n[!] Solutions:")
    print("   1. Make sure virtual environment is activated")
    print("   2. Run: pip install -r requirements.txt")
    print("   3. If using Python 3.13, see PYTHON_313_COMPATIBILITY.md")
    print("   4. Consider using Python 3.11 or 3.12 instead")
    print("\n   For Python 3.13 users:")
    print("   pip install --upgrade pip")
    print("   pip install -r requirements.txt --no-cache-dir")
else:
    print("\n[SUCCESS] All packages are installed correctly!")
    print("   You can now run: uvicorn main:app --reload")

print("\n" + "=" * 60)
