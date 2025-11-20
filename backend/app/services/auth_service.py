from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.auth import UserRegister
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.validators import is_valid_email, is_strong_password, is_valid_username

class AuthService:
    @staticmethod
    def user_exists(db: Session, email: str) -> bool:
        """Verifica se usuário com email já existe"""
        return db.query(User).filter(User.email == email).first() is not None
    
    @staticmethod
    def username_exists(db: Session, username: str) -> bool:
        """Verifica se username já existe"""
        return db.query(User).filter(User.username == username).first() is not None
    
    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        """Cria novo usuário"""
        is_valid, error_msg = is_valid_username(user_data.username)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        is_valid, error_msg = is_strong_password(user_data.password)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        if AuthService.user_exists(db, user_data.email):
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado"
            )
        
        if AuthService.username_exists(db, user_data.username):
            raise HTTPException(
                status_code=400,
                detail="Username já está em uso"
            )
        
        password_truncated = user_data.password[:72]
        
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(password_truncated) 
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> User | None:
        """Autentica usuário"""
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            return None
        
        password_truncated = password[:72]
        
        if not verify_password(password_truncated, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Busca usuário por ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Busca usuário por email"""
        return db.query(User).filter(User.email == email).first()