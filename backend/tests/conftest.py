import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.utils.security import create_access_token


@pytest.fixture(scope="session")
def engine():
    """Cria engine do banco de dados de teste em memória"""
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Cria sessão de banco isolada para cada teste"""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de teste do FastAPI com banco sobrescrito"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Dados válidos para criação de usuário"""
    return {
        "username": "testuser",
        "email": "test@test.com",
        "password": "senha123"
    }


@pytest.fixture
def authenticated_user(db_session, sample_user_data):
    """Cria usuário autenticado no banco"""
    from app.services.auth_service import AuthService
    from app.schemas.auth import UserRegister
    
    user_register = UserRegister(**sample_user_data)
    user = AuthService.create_user(db_session, user_register)
    return user


@pytest.fixture
def auth_token(authenticated_user):
    """Gera token JWT para usuário autenticado"""
    return create_access_token(authenticated_user.id)


@pytest.fixture
def auth_headers(auth_token):
    """Headers HTTP com token de autenticação"""
    return {"Authorization": f"Bearer {auth_token}"}