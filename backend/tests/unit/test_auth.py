import pytest

def test_register_user_success(client, sample_user_data):
    """Teste: Registrar usuário com sucesso"""
    response = client.post("/api/auth/register", json=sample_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == sample_user_data["username"]
    assert data["email"] == sample_user_data["email"]
    assert "id" in data

def test_register_duplicate_email(client, sample_user_data):
    """Teste: Não pode registrar email duplicado"""
    # Primeiro registro
    client.post("/api/auth/register", json=sample_user_data)
    
    # Segundo registro com mesmo email
    response = client.post("/api/auth/register", json=sample_user_data)
    
    assert response.status_code == 400
    assert "já cadastrado" in response.json()["detail"].lower()

def test_login_success(client, sample_user_data):
    """Teste: Login com credenciais corretas"""
    # Registrar
    client.post("/api/auth/register", json=sample_user_data)
    
    # Login
    response = client.post("/api/auth/login", json={
        "email": sample_user_data["email"],
        "password": sample_user_data["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data

def test_login_wrong_password(client, sample_user_data):
    """Teste: Login com senha incorreta"""
    # Registrar
    client.post("/api/auth/register", json=sample_user_data)
    
    # Login com senha errada
    response = client.post("/api/auth/login", json={
        "email": sample_user_data["email"],
        "password": "senhaerrada"
    })
    
    assert response.status_code == 401

def test_get_me_with_valid_token(client, auth_headers):
    """Teste: Acessar /me com token válido"""
    response = client.get("/api/auth/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "username" in data

def test_get_me_without_token(client):
    """Teste: Acessar /me sem token"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401