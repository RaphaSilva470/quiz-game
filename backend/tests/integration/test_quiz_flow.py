import pytest
from app.models.question import Question


@pytest.fixture
def quiz_questions(db_session):
    """Fixture: cria 5 perguntas de geografia no banco"""
    questions = []
    for i in range(5):
        q = Question(
            text=f"Pergunta {i+1}?",
            category="geografia",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation=f"Explicação {i+1}"
        )
        db_session.add(q)
        questions.append(q)
    
    db_session.commit()
    
    # 1. Iniciar quiz a
    response = client.post(
        "/api/quiz/start",
        json={"num_questions": 5},
        headers=auth_headers
    )
    
    assert response.status_code == 201
    quiz_data = response.json()
    quiz_id = quiz_data["quiz_id"]
    questions = quiz_data["questions"]
    
    assert len(questions) == 5
    assert "id" in questions[0]
    
    # 2. Responder todas as perguntas
    for q in questions:
        response = client.post(
            f"/api/quiz/{quiz_id}/answer",
            json={
                "question_id": q["id"],
                "answer": "A",
                "time_taken": 5.0
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        answer_data = response.json()
        assert answer_data["is_correct"] == True
    
    # 3. Finalizar quiz
    response = client.post(
        f"/api/quiz/{quiz_id}/finish",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    result = response.json()
    assert result["correct_answers"] == 5
    assert result["final_score"] == 50
    assert result["accuracy"] == 100.0
    
    # 4. Verificar histórico
    response = client.get("/api/quiz/history", headers=auth_headers)
    
    assert response.status_code == 200
    history = response.json()
    assert history["total_quizzes"] == 1
    
    # 5. Verificar ranking
    response = client.get("/api/ranking/global", headers=auth_headers)
    
    assert response.status_code == 200
    ranking = response.json()
    assert len(ranking["ranking"]) > 0