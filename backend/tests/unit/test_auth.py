import pytest
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister
from app.models.user import User


def test_user_exists_returns_true(db_session):
    """Teste unitário: user_exists retorna True quando usuário existe"""
    user = User(username="test", email="test@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    assert AuthService.user_exists(db_session, "test@test.com") == True


def test_user_exists_returns_false(db_session):
    """Teste unitário: user_exists retorna False quando não existe"""
    assert AuthService.user_exists(db_session, "naoexiste@test.com") == False


def test_username_exists_returns_true(db_session):
    """Teste unitário: username_exists retorna True quando existe"""
    user = User(username="joao", email="joao@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    assert AuthService.username_exists(db_session, "joao") == True


def test_username_exists_returns_false(db_session):
    """Teste unitário: username_exists retorna False quando não existe"""
    assert AuthService.username_exists(db_session, "naoexiste") == False


def test_create_user_success(db_session):
    """Teste unitário: create_user cria usuário com sucesso"""
    user_data = UserRegister(
        username="newuser",
        email="new@test.com",
        password="senha123"
    )
    
    user = AuthService.create_user(db_session, user_data)
    
    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "new@test.com"
    assert user.password_hash != "senha123"  # Hash aplicado


def test_create_user_duplicate_email_raises_exception(db_session):
    """Teste unitário: create_user lança exceção para email duplicado"""
    # Criar primeiro usuário
    user1 = UserRegister(username="user1", email="same@test.com", password="senha123")
    AuthService.create_user(db_session, user1)
    
    # Tentar criar segundo com mesmo email
    user2 = UserRegister(username="user2", email="same@test.com", password="senha123")
    
    with pytest.raises(HTTPException) as exc_info:
        AuthService.create_user(db_session, user2)
    
    assert exc_info.value.status_code == 400
    assert "já cadastrado" in exc_info.value.detail.lower()


def test_get_user_by_id_returns_user(db_session):
    """Teste unitário: get_user_by_id retorna usuário quando existe"""
    user = User(username="test", email="test@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    found_user = AuthService.get_user_by_id(db_session, user.id)
    
    assert found_user is not None
    assert found_user.id == user.id


def test_get_user_by_email_returns_user(db_session):
    """Teste unitário: get_user_by_email retorna usuário quando existe"""
    user = User(username="test", email="test@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    found_user = AuthService.get_user_by_email(db_session, "test@test.com")
    
    assert found_user is not None
    assert found_user.email == "test@test.com"