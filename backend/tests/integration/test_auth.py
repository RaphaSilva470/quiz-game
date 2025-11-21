import pytest


@pytest.fixture
def valid_user_data():
    """Fixture: dados válidos de usuário para testes"""
    return {
        "username": "testuser",
        "email": "test@test.com",
        "password": "senha123"
    }


class TestAuthenticationFlow:
    """Testes de integração para fluxo de autenticação"""
    
    def test_should_complete_full_authentication_flow(self, client, valid_user_data):
        """Fluxo completo: registro → login → acesso a recurso protegido"""
        
        register_response = client.post("/api/auth/register", json=valid_user_data)
        assert register_response.status_code == 201
        
        login_response = client.post("/api/auth/login", json={
            "email": valid_user_data["email"],
            "password": valid_user_data["password"]
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        me_response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == 200
        
        user_data = me_response.json()
        assert user_data["email"] == valid_user_data["email"]
        assert user_data["username"] == valid_user_data["username"]
    
    def test_should_reject_login_with_invalid_credentials(self, client):
        """Tentativa de login com credenciais inválidas deve falhar"""
        
        client.post("/api/auth/register", json={
            "username": "user",
            "email": "user@test.com",
            "password": "senha123"
        })
        
        response = client.post("/api/auth/login", json={
            "email": "user@test.com",
            "password": "senhaerrada"
        })
        
        assert response.status_code == 401