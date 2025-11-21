import pytest
from app.models.question import Question
from app.models.user import User

def test_ranking_after_multiple_quizzes(client, db_session):
    """Teste E2E: Ranking após múltiplos quizzes"""
    
    # Adicionar perguntas
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
    db_session.commit()
    
    # Criar 2 usuários
    users = []
    for i in range(2):
        user_data = {
            "username": f"user{i}",
            "email": f"user{i}@test.com",
            "password": "senha123"
        }
        client.post("/api/auth/register", json=user_data)
        
        response = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        token = response.json()["access_token"]
        users.append({"headers": {"Authorization": f"Bearer {token}"}})
    
    # User 0 faz 2 quizzes
    for _ in range(2):
        response = client.post(
            "/api/quiz/start",
            json={"num_questions": 5},
            headers=users[0]["headers"]
        )
        quiz_id = response.json()["quiz_id"]
        questions = response.json()["questions"]
        
        for q in questions:
            client.post(
                f"/api/quiz/{quiz_id}/answer",
                json={"question_id": q["id"], "answer": "A", "time_taken": 3.0},
                headers=users[0]["headers"]
            )
        
        client.post(
            f"/api/quiz/{quiz_id}/finish",
            headers=users[0]["headers"]
        )
    
    # User 1 faz 1 quiz
    response = client.post(
        "/api/quiz/start",
        json={"num_questions": 5},
        headers=users[1]["headers"]
    )
    quiz_id = response.json()["quiz_id"]
    questions = response.json()["questions"]
    
    for q in questions:
        client.post(
            f"/api/quiz/{quiz_id}/answer",
            json={"question_id": q["id"], "answer": "A", "time_taken": 3.0},
            headers=users[1]["headers"]
        )
    
    client.post(
        f"/api/quiz/{quiz_id}/finish",
        headers=users[1]["headers"]
    )
    
    # Verificar ranking
    response = client.get(
        "/api/ranking/global",
        headers=users[0]["headers"]
    )
    
    assert response.status_code == 200
    ranking = response.json()["ranking"]
    
    # User 0 deve estar em primeiro (2 quizzes vs 1)
    assert len(ranking) == 2
    assert ranking[0]["username"] == "user0"
    assert ranking[0]["total_score"] > ranking[1]["total_score"]