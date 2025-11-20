import re
from typing import Optional

def is_valid_email(email: str) -> bool:
    """
    Valida formato de email
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Valida força da senha
    Retorna (is_valid, error_message)
    """
    if len(password) < 6:
        return False, "Senha deve ter no mínimo 6 caracteres"
    
    # Pode adicionar mais regras aqui:
    # - ter letra maiúscula
    # - ter número
    # - ter caractere especial
    
    return True, None

def is_valid_username(username: str) -> tuple[bool, Optional[str]]:
    """
    Valida username
    """
    if len(username) < 3:
        return False, "Username deve ter no mínimo 3 caracteres"
    
    if len(username) > 50:
        return False, "Username deve ter no máximo 50 caracteres"
    
    # Apenas letras, números e underscore
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username deve conter apenas letras, números e underscore"
    
    return True, None

def is_valid_category(category: Optional[str]) -> bool:
    """
    Valida categoria de pergunta
    """
    valid_categories = ["geografia", "historia", "ciencias", "esportes", "geral", None]
    return category in valid_categories

def is_valid_difficulty(difficulty: Optional[str]) -> bool:
    """
    Valida dificuldade de pergunta
    """
    valid_difficulties = ["facil", "medio", "dificil", None]
    return difficulty in valid_difficulties