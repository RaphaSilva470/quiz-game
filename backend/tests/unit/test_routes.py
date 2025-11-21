import pytest
from fastapi import status

class TestAuthRoutes:
    """Testes para rotas de autenticação"""
    
    def test_register_missing_fields(self, client):
        """Teste: Registrar sem campos obrigatórios"""
        response = client.post("/api/auth/register", json={
            "username": "test"
            # Faltando email e password
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_register_invalid_email_format(self, client):
        """Teste: Registrar com email inválido"""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "invalid-email",
            "password": "senha123"
        })
        
        assert response.status_code == 422
    
    def test_register_weak_password(self, client):
        """Teste: Registrar com senha fraca"""
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "12345"  # Menos de 6 caracteres
        })
        
        assert response.status_code == 422
        assert "mínimo 6" in response.json()["detail"].lower()
    
    def test_register_invalid_username(self, client):
        """Teste: Registrar com username inválido"""
        response = client.post("/api/auth/register", json={
            "username": "ab",  # Muito curto
            "email": "test@test.com",
            "password": "senha123"
        })
        
        assert response.status_code == 422
    
    def test_login_missing_credentials(self, client):
        """Teste: Login sem credenciais"""
        response = client.post("/api/auth/login", json={
            "email": "test@test.com"
            # Faltando password
        })
        
        assert response.status_code == 422
    
    def test_login_nonexistent_user(self, client):
        """Teste: Login com usuário inexistente"""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@test.com",
            "password": "senha123"
        })
        
        assert response.status_code == 401
    
    def test_get_me_invalid_token(self, client):
        """Teste: Acessar /me com token inválido"""
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401

class TestQuizRoutes:
    """Testes para rotas de quiz"""
    
    def test_start_quiz_unauthorized(self, client):
        """Teste: Iniciar quiz sem autenticação"""
        response = client.post("/api/quiz/start", json={
            "num_questions": 5
        })
        
        assert response.status_code == 401
    
    def test_start_quiz_invalid_num_questions(self, client, auth_headers):
        """Teste: Iniciar quiz com número inválido de perguntas"""
        response = client.post(
            "/api/quiz/start",
            json={"num_questions": 0},
            headers=auth_headers
        )
        
        # Pode retornar 400 ou 422 dependendo da validação
        assert response.status_code in [400, 422]
    
    def test_answer_question_unauthorized(self, client):
        """Teste: Responder pergunta sem autenticação"""
        response = client.post("/api/quiz/1/answer", json={
            "question_id": 1,
            "answer": "A",
            "time_taken": 3.0
        })
        
        assert response.status_code == 401
    
    def test_finish_quiz_unauthorized(self, client):
        """Teste: Finalizar quiz sem autenticação"""
        response = client.post("/api/quiz/1/finish")
        
        assert response.status_code == 401
    
    def test_get_history_unauthorized(self, client):
        """Teste: Buscar histórico sem autenticação"""
        response = client.get("/api/quiz/history")
        
        assert response.status_code == 401

class TestRankingRoutes:
    """Testes para rotas de ranking"""
    
    def test_get_global_ranking_unauthorized(self, client):
        """Teste: Buscar ranking sem autenticação"""
        response = client.get("/api/ranking/global")
        
        assert response.status_code == 401
    
    def test_get_global_ranking_invalid_limit(self, client, auth_headers):
        """Teste: Buscar ranking com limit inválido"""
        response = client.get(
            "/api/ranking/global?limit=100",  # Máximo é 50
            headers=auth_headers
        )
        
        assert response.status_code == 422
    
    def test_get_category_ranking_unauthorized(self, client):
        """Teste: Buscar ranking por categoria sem autenticação"""
        response = client.get("/api/ranking/category/geografia")
        
        assert response.status_code == 401
    
    def test_get_category_ranking_invalid_category(self, client, auth_headers):
        """Teste: Buscar ranking com categoria inválida"""
        response = client.get(
            "/api/ranking/category/invalid_category",
            headers=auth_headers
        )
        
        assert response.status_code == 400

