from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Answer(Base):
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_session_id = Column(Integer, ForeignKey("quiz_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String(200), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Float, default=0.0)  
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    quiz_session = relationship("QuizSession", back_populates="answers")
    question = relationship("Question", back_populates="answers")