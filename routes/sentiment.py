from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from services.openai_service import openai_service
from services.data_service import generate_social_media_samples
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.database import get_db
from models.sentiment import Sentiment
import json
import time

router = APIRouter(prefix="/api/sentiment", tags=["sentiment"])

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    texts: Optional[List[str]] = None
    source: Optional[str] = 'api'

@router.post('/analyze')
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    texts = []
    if req.text:
        texts = [req.text]
    if req.texts:
        texts = req.texts
    if not texts:
        raise HTTPException(status_code=400, detail="No text provided")

    # For demo, analyze first text and store the result
    analysis = openai_service.analyze_sentiment(texts[0])

    sentiment_record = Sentiment(
        text=texts[0],
        sentiment=analysis.get('sentiment'),
        confidence=analysis.get('confidence'),
        summary=analysis.get('summary'),
        source=req.source,
        vehicle_model=analysis.get('vehicle_mentioned')
    )
    db.add(sentiment_record)
    db.flush()

    # Normalize topics into Topic table and associate
    topics = analysis.get('topics') or []
    for tname in topics:
        tname_clean = tname.strip().lower()
        topic = db.query(__import__('models.topic', fromlist=['Topic']).topic.Topic).filter_by(name=tname_clean).first()
        if not topic:
            topic = __import__('models.topic', fromlist=['Topic']).topic.Topic(name=tname_clean)
            db.add(topic)
            db.flush()
        sentiment_record.topics.append(topic)

    db.commit()
    db.refresh(sentiment_record)

    return {"success": True, "data": analysis, "record_id": sentiment_record.id}

@router.get('/summary')
async def summary(date_range: Optional[str] = 'last_30_days', vehicle_model: Optional[str] = None):
    # For demo, aggregate mock data
    samples = generate_social_media_samples(500)
    total = len(samples)
    pos = sum(1 for s in samples if s['sentiment']=='positive')
    neg = sum(1 for s in samples if s['sentiment']=='negative')
    neu = total - pos - neg
    top_pos = [s for s in samples if s['sentiment']=='positive'][:5]
    top_neg = [s for s in samples if s['sentiment']=='negative'][:5]
    trending = ["design","mileage","service"]
    return {
        "total_mentions": total,
        "positive": round(pos/total*100,2),
        "negative": round(neg/total*100,2),
        "neutral": round(neu/total*100,2),
        "top_positive_comments": top_pos,
        "top_negative_comments": top_neg,
        "trending_topics": trending
    }

@router.get('/topics')
async def topics(date_range: Optional[str] = 'last_30_days'):
    samples = generate_social_media_samples(500)
    topics = ["design","mileage","service","safety"]
    return {"trending_topics": topics}

def event_stream():
    for i in range(30):
        data = {"time": time.time(), "sentiment_score": 60 + i%10}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(0.5)

@router.get('/real-time')
async def real_time():
    return StreamingResponse(event_stream(), media_type='text/event-stream')
