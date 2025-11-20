from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ScoreResponse(BaseModel):
    id: int
    user_id: int
    quiz_session_id: int
    total_score: int
    correct_answers: int
    total_questions: int
    accuracy: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class RankingUser(BaseModel):
    position: int
    user_id: int
    username: str
    total_score: int
    total_quizzes: int
    correct_answers: int
    total_questions: int
    accuracy: float

class RankingResponse(BaseModel):
    ranking: List[RankingUser]
    user_position: int
    total_users: int

class UserStats(BaseModel):
    user_id: int
    username: str
    overall: Dict
    by_difficulty: Dict
    by_category: Dict
    recent_performance: List[Dict]

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