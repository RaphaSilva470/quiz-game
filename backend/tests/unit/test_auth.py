import pytest
from fastapi import HTTPException
from app.services.auth_service import AuthService
from app.schemas.auth import UserRegister
from app.models.user import User


@pytest.fixture
def existing_user(db_session):
    """Fixture: cria um usuário no banco de dados"""
    user = User(
        username="testuser",
        email="test@test.com",
        password_hash="hashed_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


class TestUserExists:
    """Testes para AuthService.user_exists"""
    
    def test_should_return_true_when_user_exists(self, db_session, existing_user):
        result = AuthService.user_exists(db_session, existing_user.email)
        assert result is True
    
    def test_should_return_false_when_user_does_not_exist(self, db_session):
        result = AuthService.user_exists(db_session, "naoexiste@test.com")
        assert result is False


class TestUsernameExists:
    """Testes para AuthService.username_exists"""
    
    def test_should_return_true_when_username_exists(self, db_session, existing_user):
        result = AuthService.username_exists(db_session, existing_user.username)
        assert result is True
    
    def test_should_return_false_when_username_does_not_exist(self, db_session):
        result = AuthService.username_exists(db_session, "naoexiste")
        assert result is False


class TestCreateUser:
    """Testes para AuthService.create_user"""
    
    def test_should_create_user_successfully(self, db_session):
        user_data = UserRegister(
            username="newuser",
            email="new@test.com",
            password="senha123"
        )
        
        user = AuthService.create_user(db_session, user_data)
        
        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "new@test.com"
        assert user.password_hash != "senha123"
    
    def test_should_raise_exception_when_email_already_exists(self, db_session):
        user1 = UserRegister(username="user1", email="same@test.com", password="senha123")
        AuthService.create_user(db_session, user1)
        
        user2 = UserRegister(username="user2", email="same@test.com", password="senha123")
        
        with pytest.raises(HTTPException) as exc_info:
            AuthService.create_user(db_session, user2)
        
        assert exc_info.value.status_code == 400
        assert "já cadastrado" in exc_info.value.detail.lower()


class TestGetUserById:
    """Testes para AuthService.get_user_by_id"""
    
    def test_should_return_user_when_exists(self, db_session, existing_user):
        found_user = AuthService.get_user_by_id(db_session, existing_user.id)
        
        assert found_user is not None
        assert found_user.id == existing_user.id


class TestGetUserByEmail:
    """Testes para AuthService.get_user_by_email"""
    
    def test_should_return_user_when_exists(self, db_session, existing_user):
        found_user = AuthService.get_user_by_email(db_session, existing_user.email)
        
        assert found_user is not None
        assert found_user.email == existing_user.email


class TestAuthenticate:
    """Testes para AuthService.authenticate"""
    
    def test_should_authenticate_user_with_correct_password(self, db_session):
        """Deve autenticar usuário com senha correta"""
        from app.utils.security import hash_password
        
        user_data = UserRegister(
            username="authuser",
            email="auth@test.com",
            password="senha123"
        )
        user = AuthService.create_user(db_session, user_data)
        
        authenticated = AuthService.authenticate(db_session, "auth@test.com", "senha123")
        
        assert authenticated is not None
        assert authenticated.id == user.id
        assert authenticated.email == user.email
    
    def test_should_return_none_with_incorrect_password(self, db_session):
        """Deve retornar None com senha incorreta"""
        user_data = UserRegister(
            username="authuser2",
            email="auth2@test.com",
            password="senha123"
        )
        AuthService.create_user(db_session, user_data)
        
        authenticated = AuthService.authenticate(db_session, "auth2@test.com", "senhaerrada")
        
        assert authenticated is None
    
    def test_should_return_none_when_user_does_not_exist(self, db_session):
        """Deve retornar None quando usuário não existe"""
        authenticated = AuthService.authenticate(db_session, "naoexiste@test.com", "senha123")
        
        assert authenticated is None