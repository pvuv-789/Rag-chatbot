"""
Question Answering Module
Handles RAG-based question answering using Gemini
Compatible with Python 3.11+
"""

from __future__ import annotations
import google.generativeai as genai
from typing import List, Dict, Any
from langchain_core.documents import Document


class QASystem:
    """Handles question answering using RAG with Gemini"""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize the QA system

        Args:
            api_key: Google Gemini API key
            model_name: Gemini model to use (gemini-1.5-pro or gemini-1.5-flash)
        """
        self.api_key = api_key
        self.model_name = model_name

        # Configure Gemini
        genai.configure(api_key=api_key)

        # Initialize model
        self.model = genai.GenerativeModel(model_name)

        # Generation config
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

    def create_prompt(self, question: str, context_docs: List[Document]) -> str:
        """
        Create a prompt combining context and question

        Args:
            question: User's question
            context_docs: Relevant documents from vector search

        Returns:
            Formatted prompt string
        """
        # Extract text from documents
        context_texts = [doc.page_content for doc in context_docs]
        context = "\n\n".join(context_texts)

        prompt = f"""You are an intelligent AI assistant with access to specific document context.
Your task is to answer the user's question based on the provided context.

Context:
{context}

Question:
{question}

Instructions:
- Answer the question using ONLY the information provided in the context above
- If the context doesn't contain enough information to answer the question, say "I don't have enough information in the provided documents to answer this question."
- Be concise and accurate
- If relevant, cite specific information from the context
- Maintain a helpful and professional tone

Answer:"""

        return prompt

    def generate_answer(
        self,
        question: str,
        context_docs: List[Document]
    ) -> Dict[str, Any]:
        """
        Generate an answer to the question using RAG

        Args:
            question: User's question
            context_docs: Relevant documents from vector search

        Returns:
            Dictionary containing answer and source documents
        """
        try:
            # Create prompt
            prompt = self.create_prompt(question, context_docs)

            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )

            # Extract answer
            answer = response.text

            # Extract source texts
            sources = [doc.page_content for doc in context_docs]

            return {
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")

    def chat(self, question: str, context_docs: List[Document]) -> str:
        """
        Simple chat interface - returns just the answer text

        Args:
            question: User's question
            context_docs: Relevant documents from vector search

        Returns:
            Answer text
        """
        result = self.generate_answer(question, context_docs)
        return result["answer"]
