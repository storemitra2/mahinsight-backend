from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.openai_service import openai_service
from services.data_service import generate_social_media_samples, generate_sales_data
from services.rag_service import RAGService
import json
from sqlalchemy.orm import Session
from database.database import get_db
from models.executive_chat import ExecutiveChat
from typing import List

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

class QueryRequest(BaseModel):
    question: str
    context: str = 'last_7_days'


@router.post('/query')
async def query(req: QueryRequest, db: Session = Depends(get_db)):
    rag = RAGService(db=db)
    context = rag.get_relevant_context(req.question)
    prompt = f"You are MAHInsight AI. Use this context: {json.dumps(context)}\nQuestion: {req.question}\nReturn JSON with answer, confidence, follow_up."
    ai = openai_service.executive_summary(req.question, json.dumps(context))

    # Persist chat
    chat = ExecutiveChat(question=req.question, answer=ai.get('answer') or ai.get('answer',''), context_used=str(list(context.keys())))
    db.add(chat)
    db.commit()
    db.refresh(chat)

    return {
        "answer": ai.get('answer',''),
        "data_sources": ["twitter","sales","reviews"],
        "confidence": ai.get('confidence', 0.9),
        "follow_up_questions": ai.get('follow_up', ["Would you like sales data for Thar?","Should I analyze competitor vehicles?"]),
        "record_id": chat.id
    }
