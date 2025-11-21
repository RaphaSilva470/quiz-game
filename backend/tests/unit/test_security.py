import pytest
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


def test_hash_password_returns_different_from_plain():
    """Teste unitário: hash_password gera hash diferente da senha"""
    password = "senha123"
    hashed = hash_password(password)
    
    assert hashed != password
    assert len(hashed) > 20


def test_hash_password_same_input_different_output():
    """Teste unitário: hash_password gera hashes diferentes para mesma senha"""
    password = "senha123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Hashes devem ser diferentes (salt aleatório)
    assert hash1 != hash2


def test_verify_password_correct_password():
    """Teste unitário: verify_password aceita senha correta"""
    password = "senha123"
    hashed = hash_password(password)
    
    assert verify_password(password, hashed) == True


def test_verify_password_incorrect_password():
    """Teste unitário: verify_password rejeita senha incorreta"""
    password = "senha123"
    hashed = hash_password(password)
    
    assert verify_password("senhaerrada", hashed) == False


def test_create_access_token_returns_string():
    """Teste unitário: create_access_token retorna token válido"""
    user_id = 1
    token = create_access_token(user_id)
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 20


def test_verify_token_valid_token():
    """Teste unitário: verify_token valida token correto"""
    user_id = 42
    token = create_access_token(user_id)
    
    decoded_id = verify_token(token)
    
    assert decoded_id == user_id


def test_verify_token_invalid_token():
    """Teste unitário: verify_token rejeita token inválido"""
    invalid_token = "token.invalido.aqui"
    
    decoded_id = verify_token(invalid_token)
    
    assert decoded_id is None