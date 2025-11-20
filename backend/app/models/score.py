from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Score(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"), unique=True, nullable=False)
    total_score = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    accuracy = Column(Float, nullable=False)  
    total_time = Column(Float, default=0.0)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="scores")
    quiz_session = relationship("QuizSession", back_populates="score")