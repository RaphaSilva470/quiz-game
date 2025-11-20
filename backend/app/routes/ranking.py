from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.score import RankingResponse
from app.services.score_service import ScoreService
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/ranking", tags=["Ranking"])

@router.get("/global", response_model=RankingResponse)
def get_global_ranking(
    limit: int = Query(default=10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar ranking global
    
    - **limit**: Número máximo de usuários no ranking (padrão 10, máx 50)
    """
    try:
        ranking = ScoreService.get_global_ranking(db, limit)
        
        user_position = ScoreService.get_user_position(db, current_user.id)
        
        from app.models.score import Score
        total_users = db.query(Score.user_id).distinct().count()
        
        return {
            "ranking": ranking,
            "user_position": user_position,
            "total_users": total_users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar ranking: {str(e)}"
        )

@router.get("/category/{category}")
def get_category_ranking(
    category: str,
    limit: int = Query(default=100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar ranking por categoria
    
    Categorias válidas: geografia, historia, ciencias, esportes, geral
    """
    from app.utils.validators import is_valid_category
    from app.models.score import Score
    from app.models.quiz import QuizSession
    from app.models.user import User as UserModel
    from sqlalchemy import func, desc
    
    if not is_valid_category(category):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria inválida"
        )
    
    try:
        ranking = db.query(
            UserModel.id,
            UserModel.username,
            func.sum(Score.total_score).label("category_score"),
            func.count(Score.id).label("category_quizzes"),
            func.avg(Score.accuracy).label("category_accuracy")
        ).join(
            Score, UserModel.id == Score.user_id
        ).join(
            QuizSession, Score.quiz_session_id == QuizSession.id
        ).filter(
            QuizSession.category == category
        ).group_by(
            UserModel.id, UserModel.username
        ).order_by(
            desc("category_score")
        ).limit(limit).all()
        
        result = []
        for position, row in enumerate(ranking, start=1):
            result.append({
                "position": position,
                "user_id": row.id,
                "username": row.username,
                "category_score": row.category_score or 0,
                "category_quizzes": row.category_quizzes or 0,
                "category_accuracy": round(row.category_accuracy or 0, 1)
            })
        
        user_score = db.query(
            func.sum(Score.total_score)
        ).join(
            QuizSession, Score.quiz_session_id == QuizSession.id
        ).filter(
            Score.user_id == current_user.id,
            QuizSession.category == category
        ).scalar() or 0
        
        user_position = db.query(
            Score.user_id
        ).join(
            QuizSession, Score.quiz_session_id == QuizSession.id
        ).filter(
            QuizSession.category == category
        ).group_by(
            Score.user_id
        ).having(
            func.sum(Score.total_score) > user_score
        ).count() + 1
        
        total_users = db.query(Score.user_id).join(
            QuizSession
        ).filter(
            QuizSession.category == category
        ).distinct().count()
        
        return {
            "category": category,
            "ranking": result,
            "user_position": user_position,
            "total_users": total_users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar ranking: {str(e)}"
        )