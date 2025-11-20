from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from typing import List, Optional
from app.models.quiz import QuizSession
from app.models.question import Question
from app.models.answer import Answer
from app.utils.validators import is_valid_category, is_valid_difficulty
import random

class QuizService:
    @staticmethod
    def get_random_questions(
        db: Session,
        num_questions: int,
        category: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Question]:
        """Busca perguntas aleatórias com filtros opcionais"""
        
        if category and not is_valid_category(category):
            raise HTTPException(status_code=400, detail="Categoria inválida")
        
        if difficulty and not is_valid_difficulty(difficulty):
            raise HTTPException(status_code=400, detail="Dificuldade inválida")
        
        query = db.query(Question).filter(Question.is_active == True)
        
        if category:
            query = query.filter(Question.category == category)
        
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)
        
        available_questions = query.all()
        
        if len(available_questions) < num_questions:
            raise HTTPException(
                status_code=400,
                detail=f"Não há perguntas suficientes. Disponíveis: {len(available_questions)}"
            )
        
        selected_questions = random.sample(available_questions, num_questions)
        
        return selected_questions
    
    @staticmethod
    def create_quiz_session(
        db: Session,
        user_id: int,
        category: Optional[str],
        difficulty: Optional[str],
        num_questions: int
    ) -> QuizSession:
        """Cria nova sessão de quiz"""
        
        # Criar quiz session
        quiz_session = QuizSession(
            user_id=user_id,
            total_questions=num_questions,
            category=category,
            difficulty=difficulty
        )
        
        db.add(quiz_session)
        db.commit()
        db.refresh(quiz_session)
        
        return quiz_session
    
    @staticmethod
    def get_quiz_session(db: Session, quiz_id: int, user_id: int) -> QuizSession:
        """Busca quiz session e valida que pertence ao usuário"""
        quiz = db.query(QuizSession).filter(QuizSession.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz não encontrado")
        
        if quiz.user_id != user_id:
            raise HTTPException(status_code=403, detail="Acesso negado")
        
        return quiz
    
    @staticmethod
    def record_answer(
        db: Session,
        quiz_session: QuizSession,
        question_id: int,
        user_answer: str,
        time_taken: float
    ) -> tuple[bool, Question]:
        """Registra resposta do usuário"""
        
        if quiz_session.is_completed:
            raise HTTPException(status_code=400, detail="Quiz já foi finalizado")
        
        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Pergunta não encontrada")
        
        existing_answer = db.query(Answer).filter(
            Answer.quiz_session_id == quiz_session.id,
            Answer.question_id == question_id
        ).first()
        
        if existing_answer:
            raise HTTPException(status_code=400, detail="Pergunta já foi respondida")
        
        is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
        
        answer = Answer(
            quiz_session_id=quiz_session.id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_taken=time_taken
        )
        
        db.add(answer)
        db.commit()
        
        return is_correct, question
    
    @staticmethod
    def get_quiz_progress(db: Session, quiz_session: QuizSession) -> dict:
        """Retorna progresso do quiz"""
        
        answers_count = db.query(Answer).filter(
            Answer.quiz_session_id == quiz_session.id
        ).count()
        
        correct_count = db.query(Answer).filter(
            Answer.quiz_session_id == quiz_session.id,
            Answer.is_correct == True
        ).count()
        
        current_score = correct_count * 10
        
        return {
            "questions_answered": answers_count,
            "questions_remaining": quiz_session.total_questions - answers_count,
            "correct_answers": correct_count,
            "current_score": current_score,
            "has_next_question": answers_count < quiz_session.total_questions
        }