from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    category = Column(String(50), index=True, nullable=False) 
    difficulty = Column(String(20), index=True, nullable=False)  
    question_type = Column(String(20), nullable=False)
    options = Column(JSON, nullable=False) 
    correct_answer = Column(String(200), nullable=False)
    explanation = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    answers = relationship("Answer", back_populates="question")