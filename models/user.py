from sqlalchemy import Column, Integer, String, DateTime, func, Index
from sqlalchemy.orm import relationship
from database.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # relationships
    chats = relationship('ExecutiveChat', back_populates='user')

Index('ix_user_email', User.email)
