from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

# Association table for many-to-many relationship
sentiment_topics = Table(
    'sentiment_topics',
    Base.metadata,
    Column('sentiment_id', Integer, ForeignKey('sentiments.id')),
    Column('topic_id', Integer, ForeignKey('topics.id'))
)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Relationship
    sentiments = relationship("Sentiment", secondary=sentiment_topics, back_populates="topics")
