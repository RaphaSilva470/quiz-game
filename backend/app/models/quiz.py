from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class QuizSession(Base):
    __tablename__ = "quiz_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)
    is_completed = Column(Boolean, default=False)
    total_questions = Column(Integer, nullable=False)
    category = Column(String(50), nullable=True) 
    difficulty = Column(String(20), nullable=True)  
    
    user = relationship("User", back_populates="quiz_sessions")
    answers = relationship("Answer", back_populates="quiz_session", cascade="all, delete-orphan")
    score = relationship("Score", back_populates="quiz_session", uselist=False)