"""
Quick syntax and import test for Python 3.11 compatibility
"""

from __future__ import annotations
import sys

print(f"Python Version: {sys.version}")
print(f"Python Version Info: {sys.version_info}\n")

# Test imports
try:
    print("Testing main.py imports...")
    from utils.loader import DocumentLoader
    from utils.vectorstore import VectorStore
    from utils.qa import QASystem
    print("[OK] All utility modules imported successfully\n")

    print("Testing type annotations...")
    from typing import List, Dict, Any, Optional
    print("[OK] Type annotations imported successfully\n")

    print("Testing FastAPI...")
    from fastapi import FastAPI
    from pydantic import BaseModel
    print("[OK] FastAPI and Pydantic imported successfully\n")

    print("=" * 60)
    print("[SUCCESS] All Python 3.11 compatibility tests passed!")
    print("=" * 60)

except ImportError as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[FAIL] Error: {e}")
    sys.exit(1)
