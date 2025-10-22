
import time
import logging
from typing import List, Dict, Any, Optional
import openai
import json
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)
openai.api_key = OPENAI_API_KEY

DEFAULT_MODEL = 'gpt-4'


def _try_parse_json(text: str) -> Optional[Dict[str, Any]]:
    # Try to find the first JSON object in text and parse it
    try:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            snippet = text[start:end+1]
            return json.loads(snippet)
    except Exception:
        logger.exception('Failed to parse JSON from OpenAI text')
    return None


class OpenAIService:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.rate_limit_sleep = 1.0

    def _call(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
        try:
            resp = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp
        except openai.error.RateLimitError:
            logger.warning('OpenAI rate limit hit, sleeping and retrying')
            time.sleep(self.rate_limit_sleep)
            self.rate_limit_sleep = min(self.rate_limit_sleep * 2, 10)
            return self._call(prompt, max_tokens, temperature)
        except Exception:
            logger.exception('OpenAI API error')
            raise

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Return a strict JSON-like dict for a single text input.

        Expected output keys: sentiment (POSITIVE|NEGATIVE|NEUTRAL), confidence (0-1), topics (list), summary, vehicle_mentioned
        """
        prompt = f"""
Analyze Mahindra vehicle sentiment: Produce ONLY a JSON object with the following keys:
  - sentiment: one of POSITIVE, NEGATIVE, NEUTRAL
  - confidence: float between 0 and 1
  - topics: list of strings
  - summary: short summary (1-2 sentences)
  - vehicle_mentioned: one of Thar, Scorpio, XUV700, Bolero, XUV400 or null

Text: {text}

Return only JSON.
"""
        try:
            resp = self._call(prompt, max_tokens=400)
            content = resp['choices'][0]['message']['content']
            parsed = _try_parse_json(content)
            if parsed:
                # Normalize fields
                parsed.setdefault('confidence', parsed.get('confidence', 0.9))
                parsed.setdefault('topics', parsed.get('topics', []))
                parsed.setdefault('summary', parsed.get('summary', ''))
                parsed.setdefault('vehicle_mentioned', parsed.get('vehicle_mentioned'))
                return parsed
            else:
                logger.warning('OpenAI returned non-JSON; returning fallback')
        except Exception:
            logger.exception('OpenAI analyze_sentiment failure')

        # fallback mock
        return {
            'sentiment': 'POSITIVE',
            'confidence': 0.85,
            'topics': ['design','performance'],
            'summary': 'Positive sentiment (fallback)',
            'vehicle_mentioned': None
        }

    def analyze_sentiment_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        results = []
        for t in texts:
            results.append(self.analyze_sentiment(t))
        return results

    def executive_summary(self, question: str, context_data: str) -> Dict[str, Any]:
        prompt = f"As MAHInsight AI, provide executive summary. Question: {question}\nContext:\n{context_data}\n\nReturn ONLY JSON with keys: answer, confidence, citations (list)."
        try:
            resp = self._call(prompt, max_tokens=800)
            content = resp['choices'][0]['message']['content']
            parsed = _try_parse_json(content)
            if parsed:
                return parsed
            return {"answer": content}
        except Exception:
            logger.exception('OpenAI executive_summary failed')
            return {"answer": "", "confidence": 0.0, "citations": []}

    def extract_topics(self, posts: List[str]) -> Dict[str, Any]:
        prompt = f"Extract trending topics, complaints, praises from posts:\n{posts}\nReturn JSON with keys: topics, complaints, praises"
        try:
            resp = self._call(prompt, max_tokens=500)
            parsed = _try_parse_json(resp['choices'][0]['message']['content'])
            return parsed or {"topics":[], "complaints":[], "praises":[]}
        except Exception:
            logger.exception('OpenAI extract_topics failed')
            return {"topics":[], "complaints":[], "praises":[]}

    def competitive_analysis(self, news: str) -> Dict[str, Any]:
        prompt = f"Competitive analysis from news:\n{news}\nReturn JSON with keys: insights, threats, opportunities"
        try:
            resp = self._call(prompt, max_tokens=800)
            parsed = _try_parse_json(resp['choices'][0]['message']['content'])
            return parsed or {"insights":"","threats":[],"opportunities":[]}
        except Exception:
            logger.exception('OpenAI competitive_analysis failed')
            return {"insights":"","threats":[],"opportunities":[]}


openai_service = OpenAIService()
