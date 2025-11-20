from pydantic import BaseModel, Field
from typing import Optional, List

class QuestionBase(BaseModel):
    text: str
    category: str  # geografia, historia, ciencias, esportes, geral
    difficulty: str  # facil, medio, dificil
    question_type: str  
    options: List[str]
    correct_answer: str
    explanation: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None

class QuestionResponse(BaseModel):
    id: int
    text: str
    category: str
    difficulty: str
    question_type: str
    options: List[str]
    
    class Config:
        from_attributes = True

class QuestionResponseAdmin(QuestionBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True