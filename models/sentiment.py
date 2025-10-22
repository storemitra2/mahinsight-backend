from sqlalchemy import Column, Integer, String, Float, DateTime, func, Index, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from .topic import sentiment_topics


class Sentiment(Base):
    __tablename__ = 'sentiments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(String(50), index=True)
    confidence = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)
    source = Column(String(100), nullable=True)
    vehicle_model = Column(String(100), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    topics = relationship("Topic", secondary=sentiment_topics, back_populates="sentiments")

Index('ix_sentiment_model_time', Sentiment.vehicle_model, Sentiment.timestamp)
