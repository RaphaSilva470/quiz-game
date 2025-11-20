from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.quiz import (
    QuizStart, QuizResponse, AnswerRequest, 
    AnswerResponse, QuizFinishResponse, QuizHistoryResponse, QuizHistoryItem
)
from app.schemas.question import QuestionResponse
from app.services.quiz_service import QuizService
from app.services.score_service import ScoreService
from app.dependencies import get_current_user
from app.models.user import User
from app.models.quiz import QuizSession

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

@router.post("/start", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def start_quiz(
    quiz_data: QuizStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Iniciar novo quiz
    
    - **category**: Categoria das perguntas (opcional) - geografia, historia, ciencias, esportes, geral
    - **difficulty**: Dificuldade (opcional) - facil, medio, dificil
    - **num_questions**: Número de perguntas (5-20, padrão 10)
    
    Retorna o quiz_id e todas as perguntas do quiz
    """
    try:
        questions = QuizService.get_random_questions(
            db,
            quiz_data.num_questions,
            quiz_data.category,
            quiz_data.difficulty
        )
        
        quiz_session = QuizService.create_quiz_session(
            db,
            current_user.id,
            quiz_data.category,
            quiz_data.difficulty,
            quiz_data.num_questions
        )
        
        return {
            "quiz_id": quiz_session.id,
            "user_id": quiz_session.user_id,
            "started_at": quiz_session.started_at,
            "category": quiz_session.category,
            "difficulty": quiz_session.difficulty,
            "total_questions": quiz_session.total_questions,
            "current_question_index": 0,
            "questions": [
                {
                    "id": q.id,
                    "text": q.text,
                    "category": q.category,
                    "difficulty": q.difficulty,
                    "question_type": q.question_type,
                    "options": q.options
                }
                for q in questions
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao iniciar quiz: {str(e)}"
        )

@router.post("/{quiz_id}/answer", response_model=AnswerResponse)
def answer_question(
    quiz_id: int,
    answer_data: AnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Responder uma pergunta do quiz
    
    - **question_id**: ID da pergunta
    - **answer**: Resposta do usuário
    - **time_taken**: Tempo gasto (em segundos)
    """
    try:
        quiz_session = QuizService.get_quiz_session(db, quiz_id, current_user.id)
        
        is_correct, question = QuizService.record_answer(
            db,
            quiz_session,
            answer_data.question_id,
            answer_data.answer,
            answer_data.time_taken
        )
        
        progress = QuizService.get_quiz_progress(db, quiz_session)
        
        points_earned = 10 if is_correct else 0
        
        return {
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "points_earned": points_earned,
            "current_score": progress["current_score"],
            "questions_answered": progress["questions_answered"],
            "questions_remaining": progress["questions_remaining"],
            "has_next_question": progress["has_next_question"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao responder pergunta: {str(e)}"
        )

@router.post("/{quiz_id}/finish", response_model=QuizFinishResponse)
def finish_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Finalizar quiz e calcular pontuação final
    """
    try:
        quiz_session = QuizService.get_quiz_session(db, quiz_id, current_user.id)
        
        if quiz_session.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quiz já foi finalizado"
            )
        
        score = ScoreService.calculate_and_save_score(db, quiz_session)
        
        current_position = ScoreService.get_user_position(db, current_user.id)
        
        # TODO: Calcular mudança de posição (implementar depois)
        rank_change = 0
        
        return {
            "quiz_id": quiz_session.id,
            "final_score": score.total_score,
            "total_questions": score.total_questions,
            "correct_answers": score.correct_answers,
            "incorrect_answers": score.total_questions - score.correct_answers,
            "accuracy": score.accuracy,
            "total_time": score.total_time,
            "average_time_per_question": score.total_time / score.total_questions if score.total_questions > 0 else 0,
            "rank_position": current_position,
            "rank_change": rank_change,
            "completed_at": quiz_session.finished_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao finalizar quiz: {str(e)}"
        )

@router.get("/history", response_model=QuizHistoryResponse)
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar histórico de quizzes do usuário
    """
    try:
        quiz_sessions = db.query(QuizSession).filter(
            QuizSession.user_id == current_user.id,
            QuizSession.is_completed == True
        ).order_by(QuizSession.finished_at.desc()).all()
        
        from app.models.score import Score
        
        quizzes = []
        for session in quiz_sessions:
            score = db.query(Score).filter(Score.quiz_session_id == session.id).first()
            if score:
                quizzes.append({
                    "quiz_id": session.id,
                    "category": session.category,
                    "difficulty": session.difficulty,
                    "final_score": score.total_score,
                    "correct_answers": score.correct_answers,
                    "total_questions": score.total_questions,
                    "accuracy": score.accuracy,
                    "completed_at": session.finished_at
                })
        
        return {
            "total_quizzes": len(quizzes),
            "quizzes": quizzes
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar histórico: {str(e)}"
        )