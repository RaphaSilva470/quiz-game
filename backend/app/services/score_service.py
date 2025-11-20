from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException
from app.models.score import Score
from app.models.answer import Answer
from app.models.quiz import QuizSession
from app.models.user import User
from datetime import datetime, timedelta

class ScoreService:
    @staticmethod
    def calculate_and_save_score(db: Session, quiz_session: QuizSession) -> Score:
        """Calcula e salva pontuação final do quiz"""
        
        answers = db.query(Answer).filter(
            Answer.quiz_session_id == quiz_session.id
        ).all()
        
        total_questions = len(answers)
        correct_answers = sum(1 for a in answers if a.is_correct)
        total_score = correct_answers * 10  
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        total_time = sum(a.time_taken for a in answers)
        
        score = Score(
            user_id=quiz_session.user_id,
            quiz_session_id=quiz_session.id,
            total_score=total_score,
            correct_answers=correct_answers,
            total_questions=total_questions,
            accuracy=accuracy,
            total_time=total_time
        )
        
        db.add(score)
        
        quiz_session.is_completed = True
        quiz_session.finished_at = datetime.utcnow()
        
        db.commit()
        db.refresh(score)
        
        return score
    
    @staticmethod
    def get_global_ranking(db: Session, limit: int = 100) -> list:
        """Retorna ranking global dos usuários"""
        
        ranking = db.query(
            User.id,
            User.username,
            func.sum(Score.total_score).label("total_score"),
            func.count(Score.id).label("total_quizzes"),
            func.sum(Score.correct_answers).label("correct_answers"),
            func.sum(Score.total_questions).label("total_questions"),
            func.avg(Score.accuracy).label("accuracy")
        ).join(
            Score, User.id == Score.user_id
        ).group_by(
            User.id, User.username
        ).order_by(
            desc("total_score")
        ).limit(limit).all()
        
        result = []
        for position, row in enumerate(ranking, start=1):
            result.append({
                "position": position,
                "user_id": row.id,
                "username": row.username,
                "total_score": row.total_score or 0,
                "total_quizzes": row.total_quizzes or 0,
                "correct_answers": row.correct_answers or 0,
                "total_questions": row.total_questions or 0,
                "accuracy": round(row.accuracy or 0, 1)
            })
        
        return result
    
    @staticmethod
    def get_user_position(db: Session, user_id: int) -> int:
        """Retorna posição do usuário no ranking global"""
        
        user_score = db.query(
            func.sum(Score.total_score).label("total_score")
        ).filter(
            Score.user_id == user_id
        ).scalar() or 0
        
        higher_users = db.query(
            Score.user_id
        ).group_by(
            Score.user_id
        ).having(
            func.sum(Score.total_score) > user_score
        ).count()
        
        return higher_users + 1
    
    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> dict:
        """Retorna estatísticas completas do usuário"""
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        scores = db.query(Score).filter(Score.user_id == user_id).all()
        
        if not scores:
            return {
                "user_id": user_id,
                "username": user.username,
                "overall": {
                    "total_quizzes": 0,
                    "total_questions": 0,
                    "correct_answers": 0,
                    "incorrect_answers": 0,
                    "accuracy": 0,
                    "total_score": 0,
                    "average_score": 0,
                    "best_score": 0,
                    "worst_score": 0,
                    "total_time_played": 0
                },
                "by_difficulty": {},
                "by_category": {},
                "recent_performance": []
            }
        
        total_quizzes = len(scores)
        total_questions = sum(s.total_questions for s in scores)
        correct_answers = sum(s.correct_answers for s in scores)
        total_score = sum(s.total_score for s in scores)
        total_time = sum(s.total_time for s in scores)
        
        overall = {
            "total_quizzes": total_quizzes,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "incorrect_answers": total_questions - correct_answers,
            "accuracy": round((correct_answers / total_questions * 100) if total_questions > 0 else 0, 1),
            "total_score": total_score,
            "average_score": round(total_score / total_quizzes, 1) if total_quizzes > 0 else 0,
            "best_score": max(s.total_score for s in scores),
            "worst_score": min(s.total_score for s in scores),
            "total_time_played": int(total_time)
        }
        
        by_difficulty = {}
        for difficulty in ["facil", "medio", "dificil"]:
            diff_scores = [
                s for s in scores 
                if db.query(QuizSession).filter(QuizSession.id == s.quiz_session_id).first().difficulty == difficulty
            ]
            
            if diff_scores:
                diff_questions = sum(s.total_questions for s in diff_scores)
                diff_correct = sum(s.correct_answers for s in diff_scores)
                
                by_difficulty[difficulty] = {
                    "quizzes": len(diff_scores),
                    "questions": diff_questions,
                    "correct": diff_correct,
                    "accuracy": round((diff_correct / diff_questions * 100) if diff_questions > 0 else 0, 1),
                    "average_score": round(sum(s.total_score for s in diff_scores) / len(diff_scores), 1)
                }
        
        by_category = {}
        for category in ["geografia", "historia", "ciencias", "esportes", "geral"]:
            cat_scores = [
                s for s in scores 
                if db.query(QuizSession).filter(QuizSession.id == s.quiz_session_id).first().category == category
            ]
            
            if cat_scores:
                cat_questions = sum(s.total_questions for s in cat_scores)
                cat_correct = sum(s.correct_answers for s in cat_scores)
                
                by_category[category] = {
                    "quizzes": len(cat_scores),
                    "questions": cat_questions,
                    "correct": cat_correct,
                    "accuracy": round((cat_correct / cat_questions * 100) if cat_questions > 0 else 0, 1)
                }
        
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_scores = [s for s in scores if s.created_at >= seven_days_ago]
        
        recent_performance = []
        
        return {
            "user_id": user_id,
            "username": user.username,
            "overall": overall,
            "by_difficulty": by_difficulty,
            "by_category": by_category,
            "recent_performance": recent_performance
        }