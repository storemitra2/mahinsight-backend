from typing import Dict, List
from database.database import get_db
from models.sentiment import Sentiment
from models.sales import Sales
from services.vector_store import VectorRAGService
import json


class RAGService:
    def __init__(self, db=None):
        if db is None:
            self.db = next(get_db())
            self._own_session = True
        else:
            self.db = db
            self._own_session = False
        self.vector_store = VectorRAGService()

    def build_vector_index(self):
        sentiments = self.db.query(Sentiment).order_by(Sentiment.timestamp.desc()).limit(2000).all()
        sales_data = self.db.query(Sales).order_by(Sales.date.desc()).limit(1000).all()

        texts = []
        metadata = []

        for s in sentiments:
            topics = [t.name for t in s.topics] if getattr(s, 'topics', None) else []
            text = f"{s.text} | topics: {', '.join(topics)} | sentiment: {s.sentiment}"
            texts.append(text)
            metadata.append({"type": "sentiment", "id": s.id, "vehicle": s.vehicle_model})

        for sal in sales_data:
            text = f"Sales: {sal.vehicle_model} in {sal.region} sold {sal.units_sold}"
            texts.append(text)
            metadata.append({"type": "sales", "id": sal.id, "vehicle": sal.vehicle_model, "region": sal.region})

        if texts:
            self.vector_store.build_index(texts, metadata)

    def get_relevant_context(self, question: str) -> Dict:
        # Ensure index built
        self.build_vector_index()
        vector_results = self.vector_store.search(question, k=10)

        sentiment_data = [r for r in vector_results if r['metadata']['type']=='sentiment']
        sales_data = [r for r in vector_results if r['metadata']['type']=='sales']

        return {"sentiment_data": sentiment_data, "sales_data": sales_data, "vector_results": vector_results}

    def close(self):
        if self._own_session:
            try:
                self.db.close()
            except Exception:
                pass
