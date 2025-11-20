from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings

# Usar argon2 ao invés de bcrypt
pwd_context = CryptContext(
    schemes=["argon2"],  # ← MUDOU AQUI
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """
    Cria hash da senha usando argon2
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha bate com o hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token JWT com o user_id
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "sub": str(user_id),
        "exp": expire
    }
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[int]:
    """
    Verifica e decodifica token JWT
    Retorna user_id se válido, None se inválido
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            return None
        
        return int(user_id)
    except JWTError:
        return None