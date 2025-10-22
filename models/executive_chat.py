from sqlalchemy import Column, Integer, String, DateTime, Text, func, Index, ForeignKey, Float
from sqlalchemy.orm import relationship
from database.database import Base

class ExecutiveChat(Base):
    __tablename__ = 'executive_chats'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    context_used = Column(String(500), nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    user = relationship('User', back_populates='chats')

Index('ix_chat_user_time', ExecutiveChat.user_id, ExecutiveChat.timestamp)
