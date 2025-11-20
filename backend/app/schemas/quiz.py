from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.schemas.question import QuestionResponse

class QuizStart(BaseModel):
    category: Optional[str] = None
    difficulty: Optional[str] = None
    num_questions: int = Field(default=10, ge=5, le=20)

class QuizResponse(BaseModel):
    quiz_id: int
    user_id: int
    started_at: datetime
    category: Optional[str]
    difficulty: Optional[str]
    total_questions: int
    current_question_index: int = 0
    questions: List[QuestionResponse]
    
    class Config:
        from_attributes = True

class AnswerRequest(BaseModel):
    question_id: int
    answer: str
    time_taken: float = 0.0

class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: Optional[str]
    points_earned: int
    current_score: int
    questions_answered: int
    questions_remaining: int
    has_next_question: bool

class QuizFinishResponse(BaseModel):
    quiz_id: int
    final_score: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    accuracy: float
    total_time: float
    average_time_per_question: float
    rank_position: int
    rank_change: int
    completed_at: datetime

class QuizFinishResponse(BaseModel):
    quiz_id: int
    final_score: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    accuracy: float
    total_time: float
    average_time_per_question: float
    rank_position: int
    rank_change: int
    completed_at: datetime

class QuizHistoryItem(BaseModel):
    quiz_id: int
    category: Optional[str]
    difficulty: Optional[str]
    final_score: int
    correct_answers: int
    total_questions: int
    accuracy: float
    completed_at: datetime

class QuizHistoryResponse(BaseModel):
    total_quizzes: int
    quizzes: List[QuizHistoryItem]