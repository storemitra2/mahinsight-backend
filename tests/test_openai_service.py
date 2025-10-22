import pytest
from services.openai_service import OpenAIService


class TestOpenAIService:
    def setup_method(self):
        self.service = OpenAIService()

    def test_sentiment_analysis_structure(self):
        result = self.service.analyze_sentiment("I love the Thar's design!")
        assert "sentiment" in result
        assert "confidence" in result
        assert "topics" in result
        assert "summary" in result
        assert "vehicle_mentioned" in result
        assert 0 <= result["confidence"] <= 1

    def test_fallback_on_error(self):
        result = self.service.analyze_sentiment("")
        assert result["sentiment"] in ["POSITIVE","NEGATIVE","NEUTRAL"]
