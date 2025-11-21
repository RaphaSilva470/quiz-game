import pytest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)
from app.config import settings

class TestPasswordHashing:
    """Testes para hash e verificação de senha"""
    
    def test_hash_password_creates_different_hash(self):
        """Teste: Hash de senha cria hash diferente a cada vez"""
        password = "senha123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Hashes devem ser diferentes (salt aleatório)
        assert hash1 != hash2
        assert len(hash1) > 0
        assert len(hash2) > 0
    
    def test_verify_password_correct(self):
        """Teste: Verificar senha correta"""
        password = "senha123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) == True
    
    def test_verify_password_incorrect(self):
        """Teste: Verificar senha incorreta"""
        password = "senha123"
        wrong_password = "senha456"
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) == False
    
    def test_verify_password_empty(self):
        """Teste: Verificar senha vazia"""
        password = "senha123"
        hashed = hash_password(password)
        
        assert verify_password("", hashed) == False

class TestJWTToken:
    """Testes para criação e verificação de token JWT"""
    
    def test_create_access_token(self):
        """Teste: Criar token de acesso"""
        user_id = 123
        token = create_access_token(user_id)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self):
        """Teste: Verificar token válido"""
        user_id = 123
        token = create_access_token(user_id)
        
        decoded_id = verify_token(token)
        assert decoded_id == user_id
    
    def test_verify_token_invalid(self):
        """Teste: Verificar token inválido"""
        invalid_token = "invalid.token.here"
        
        decoded_id = verify_token(invalid_token)
        assert decoded_id is None
    
    def test_verify_token_empty(self):
        """Teste: Verificar token vazio"""
        decoded_id = verify_token("")
        assert decoded_id is None
    
    def test_token_contains_user_id(self):
        """Teste: Token contém user_id correto"""
        user_id = 456
        token = create_access_token(user_id)
        
        decoded_id = verify_token(token)
        assert decoded_id == user_id

