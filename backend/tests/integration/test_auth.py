import pytest

def test_register_login_get_me_flow(client):
    """Teste E2E: Fluxo completo de autenticação"""
    
    # 1. Registrar
    user_data = {
        "username": "testuser",
        "email": "test@test.com",
        "password": "senha123"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    
    # 2. Login
    response = client.post("/api/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    # 3. Acessar /me
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

def test_invalid_credentials_flow(client):
    """Teste E2E: Tentativa de login com credenciais inválidas"""
    
    # Registrar
    client.post("/api/auth/register", json={
        "username": "user",
        "email": "user@test.com",
        "password": "senha123"
    })
    
    # Tentar login com senha errada
    response = client.post("/api/auth/login", json={
        "email": "user@test.com",
        "password": "senhaerrada"
    })
    
    assert response.status_code == 401