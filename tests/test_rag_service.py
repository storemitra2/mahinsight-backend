import pytest
from services.rag_service import RAGService


class TestRAGService:
    def test_context_retrieval(self):
        service = RAGService()
        context = service.get_relevant_context("Tell me about Thar")
        assert "sentiment_data" in context
        assert "sales_data" in context
        assert "vector_results" in context
