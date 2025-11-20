import pytest
import sys
import os

# Adicionar pasta raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Banco de teste em memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Criar banco de teste para cada teste"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cliente de teste do FastAPI"""
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
    """Dados de exemplo de usuário"""
    return {
        "username": "testuser",
        "email": "test@test.com",
        "password": "senha123"
    }

@pytest.fixture
def auth_headers(client, sample_user_data):
    """Headers com token de autenticação"""
    # Registrar usuário
    client.post("/api/auth/register", json=sample_user_data)
    
    # Fazer login
    response = client.post("/api/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}