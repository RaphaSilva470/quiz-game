from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.utils.security import create_access_token
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registrar novo usuário
    
    - **username**: Nome de usuário único (3-50 caracteres)
    - **email**: Email válido e único
    - **password**: Senha (mínimo 6 caracteres)
    """
    try:
        user = AuthService.create_user(db, user_data)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Fazer login
    
    - **email**: Email cadastrado
    - **password**: Senha
    
    Retorna token JWT que deve ser usado em rotas protegidas
    """
    user = AuthService.authenticate(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    access_token = create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Obter dados do usuário autenticado
    
    Requer token JWT no header: Authorization: Bearer <token>
    """
    return current_user