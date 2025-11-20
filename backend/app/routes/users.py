from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.score import UserStats
from app.services.score_service import ScoreService
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/users", tags=["Usuários"])

@router.get("/me/stats", response_model=UserStats)
def get_my_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar estatísticas detalhadas do usuário autenticado
    """
    try:
        stats = ScoreService.get_user_stats(db, current_user.id)
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar estatísticas: {str(e)}"
        )