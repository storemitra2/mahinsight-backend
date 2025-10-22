from sqlalchemy import Column, Integer, String, DateTime, Float, func, Index
from database.database import Base

class SocialBuzz(Base):
    __tablename__ = 'social_buzz'
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String(100), index=True)
    buzz_intensity = Column(Float, nullable=False)
    trending_model = Column(String(100), nullable=True)
    trending_topic = Column(String(200), nullable=True)
    mentions = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

Index('ix_buzz_state_time', SocialBuzz.state, SocialBuzz.timestamp)
