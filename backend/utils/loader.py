"""
PDF Document Loader Module
Handles PDF text extraction and chunking using LangChain
Compatible with Python 3.11+
"""

from __future__ import annotations
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document



class DocumentLoader:
    """Loads and processes PDF documents for RAG"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document loader

        Args:
            chunk_size: Maximum size of each text chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_pdf(self, file_path: str) -> List[Document]:
        """
        Load and process a PDF file

        Args:
            file_path: Path to the PDF file

        Returns:
            List of Document objects containing chunked text
        """
        try:
            # Load PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()

            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)

            return chunks
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")

    def load_multiple_pdfs(self, file_paths: List[str]) -> List[Document]:
        """
        Load and process multiple PDF files

        Args:
            file_paths: List of paths to PDF files

        Returns:
            Combined list of Document objects
        """
        all_chunks = []
        for file_path in file_paths:
            chunks = self.load_pdf(file_path)
            all_chunks.extend(chunks)

        return all_chunks
