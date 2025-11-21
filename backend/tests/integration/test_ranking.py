import pytest
from app.models.question import Question


@pytest.fixture
def general_questions(db_session):
    """Fixture: cria 10 perguntas gerais no banco"""
    questions = []
    for i in range(10):
        q = Question(
            text=f"Pergunta {i}?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(q)
        questions.append(q)
    
    db_session.commit()
    return questions


@pytest.fixture
def multiple_users(client):
    """Fixture: cria 2 usuários e retorna seus tokens de autenticação"""
    users = []
    for i in range(2):
        user_data = {
            "username": f"user{i}",
            "email": f"user{i}@test.com",
            "password": "senha123"
        }
        client.post("/api/auth/register", json=user_data)
        
        login_response = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        token = login_response.json()["access_token"]
        users.append({"Authorization": f"Bearer {token}"})
    
    return users


def complete_quiz(client, headers, num_questions=5):
    """Helper: completa um quiz inteiro retornando o resultado"""
    start_response = client.post(
        "/api/quiz/start",
        json={"num_questions": num_questions},
        headers=headers
    )
    quiz_id = start_response.json()["quiz_id"]
    questions = start_response.json()["questions"]
    
    for question in questions:
        client.post(
            f"/api/quiz/{quiz_id}/answer",
            json={
                "question_id": question["id"],
                "answer": "A",
                "time_taken": 3.0
            },
            headers=headers
        )
    
    finish_response = client.post(
        f"/api/quiz/{quiz_id}/finish",
        headers=headers
    )
    return finish_response.json()


class TestRankingSystem:
    """Testes de integração para sistema de ranking"""
    
    def test_should_rank_users_by_total_score(
        self, client, general_questions, multiple_users
    ):
        """Ranking deve ordenar usuários por pontuação total acumulada"""
        
        user0_headers = multiple_users[0]
        user1_headers = multiple_users[1]
        
        # User0 faz 2 quizzes
        complete_quiz(client, user0_headers)
        complete_quiz(client, user0_headers)
        
        # User1 faz 1 quiz
        complete_quiz(client, user1_headers)
        
        # Verificar ranking
        ranking_response = client.get(
            "/api/ranking/global",
            headers=user0_headers
        )
        
        assert ranking_response.status_code == 200
        ranking = ranking_response.json()["ranking"]
        
        assert len(ranking) == 2
        assert ranking[0]["username"] == "user0"
        assert ranking[0]["total_score"] > ranking[1]["total_score"]
