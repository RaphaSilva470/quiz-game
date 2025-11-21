import pytest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


class TestHashPassword:
    """Testes para hash_password"""
    
    def test_should_return_hash_different_from_plain_password(self):
        password = "senha123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 20
    
    def test_should_generate_different_hashes_for_same_password(self):
        password = "senha123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2


class TestVerifyPassword:
    """Testes para verify_password"""
    
    def test_should_accept_correct_password(self):
        password = "senha123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True
    
    def test_should_reject_incorrect_password(self):
        password = "senha123"
        hashed = hash_password(password)
        
        assert verify_password("senhaerrada", hashed) is False


class TestCreateAccessToken:
    """Testes para create_access_token"""
    
    def test_should_return_valid_token_string(self):
        user_id = 1
        token = create_access_token(user_id)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20


class TestVerifyToken:
    """Testes para verify_token"""
    
    def test_should_decode_valid_token(self):
        user_id = 42
        token = create_access_token(user_id)
        
        decoded_id = verify_token(token)
        
        assert decoded_id == user_id
    
    def test_should_reject_invalid_token(self):
        invalid_token = "token.invalido.aqui"
        
        decoded_id = verify_token(invalid_token)
        
        assert decoded_id is None