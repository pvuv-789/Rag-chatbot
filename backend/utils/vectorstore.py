"""
Vector Store Module
Handles embedding creation and ChromaDB operations
Compatible with Python 3.11+
"""

from __future__ import annotations
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Optional
from langchain_core.documents import Document
import os
import shutil


class VectorStore:
    """Manages vector embeddings and similarity search using ChromaDB"""

    def __init__(self, api_key: str = None, persist_directory: str = "./db", use_local_embeddings: bool = True):
        """
        Initialize the vector store

        Args:
            api_key: Google Gemini API key (optional if use_local_embeddings=True)
            persist_directory: Directory to persist ChromaDB data
            use_local_embeddings: Use local HuggingFace embeddings (no quota limits) instead of Google API
        """
        self.api_key = api_key
        self.persist_directory = persist_directory
        self.use_local_embeddings = use_local_embeddings

        # Initialize embeddings
        if use_local_embeddings:
            # Use local embeddings - no API quota limits
            print("Using local HuggingFace embeddings (no API quota limits)")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            # Use Google API embeddings
            if not api_key:
                raise ValueError("API key required when use_local_embeddings=False")
            print("Using Google Gemini API embeddings")
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=api_key
            )

        # Initialize or load vector store
        self.vectorstore: Optional[Chroma] = None
        self._initialize_vectorstore()

    def _initialize_vectorstore(self):
        """Initialize or load existing ChromaDB vector store"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(self.persist_directory, exist_ok=True)

            # Try to load existing vectorstore
            if os.path.exists(os.path.join(self.persist_directory, "chroma.sqlite3")):
                self.vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings
                )
                print(f"Loaded existing vector store from {self.persist_directory}")
            else:
                print("No existing vector store found. Will create on first document add.")
        except Exception as e:
            print(f"Error initializing vector store: {str(e)}")
            self.vectorstore = None

    def add_documents(self, documents: List[Document]) -> int:
        """
        Add documents to the vector store

        Args:
            documents: List of Document objects to add

        Returns:
            Number of documents added
        """
        try:
            if self.vectorstore is None:
                # Create new vectorstore
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    persist_directory=self.persist_directory
                )
            else:
                # Add to existing vectorstore
                self.vectorstore.add_documents(documents)

            # Note: persist() is deprecated in newer ChromaDB versions
            # Data is automatically persisted when persist_directory is set
            # If using older ChromaDB version, uncomment the line below:
            # self.vectorstore.persist()

            return len(documents)
        except Exception as e:
            error_msg = str(e)
            # Provide helpful error messages for common issues
            if "429" in error_msg or "quota" in error_msg.lower():
                raise Exception(
                    f"Error embedding content: {error_msg}\n\n"
                    "SOLUTION: You've exceeded the Google Gemini API quota. "
                    "Set USE_LOCAL_EMBEDDINGS=true in your .env file to use local embeddings "
                    "with no quota limits."
                )
            raise Exception(f"Error adding documents to vector store: {error_msg}")

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """
        Search for similar documents

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of most similar documents
        """
        if self.vectorstore is None:
            raise Exception("Vector store not initialized. Please add documents first.")

        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            error_msg = str(e)
            # Provide helpful error messages for common issues
            if "429" in error_msg or "quota" in error_msg.lower():
                raise Exception(
                    f"Error embedding query: {error_msg}\n\n"
                    "SOLUTION: You've exceeded the Google Gemini API quota. "
                    "Set USE_LOCAL_EMBEDDINGS=true in your .env file to use local embeddings "
                    "with no quota limits."
                )
            raise Exception(f"Error performing similarity search: {error_msg}")

    def clear_database(self) -> None:
        """Clear all documents from the vector store"""
        try:
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
                print(f"Cleared vector store at {self.persist_directory}")
                self._initialize_vectorstore()
        except Exception as e:
            raise Exception(f"Error clearing vector store: {str(e)}")

    def get_collection_count(self) -> int:
        """Get the number of documents in the vector store"""
        if self.vectorstore is None:
            return 0

        try:
            collection = self.vectorstore._collection
            return collection.count()
        except Exception as e:
            print(f"Error getting collection count: {str(e)}")
            return 0
