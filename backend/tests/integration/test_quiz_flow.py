import pytest
from app.models.question import Question

def test_complete_quiz_flow(client, db_session, auth_headers):
    """Teste E2E: Fluxo completo de quiz - iniciar, responder, finalizar"""
    
    # Adicionar perguntas
    for i in range(10):
        q = Question(
            text=f"Pergunta {i}?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation=f"Explicação {i}"
        )
        db_session.add(q)
    db_session.commit()
    
    # 1. Iniciar quiz
    response = client.post(
        "/api/quiz/start",
        json={"num_questions": 5},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    quiz_id = data["quiz_id"]
    questions = data["questions"]
    assert len(questions) == 5
    
    # 2. Responder todas as perguntas
    for question in questions:
        response = client.post(
            f"/api/quiz/{quiz_id}/answer",
            json={
                "question_id": question["id"],
                "answer": "A",  # Resposta correta
                "time_taken": 3.0
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        answer_data = response.json()
        assert answer_data["is_correct"] == True
        assert answer_data["points_earned"] == 10
    
    # 3. Finalizar quiz
    response = client.post(
        f"/api/quiz/{quiz_id}/finish",
        headers=auth_headers
    )
    assert response.status_code == 200
    finish_data = response.json()
    assert finish_data["final_score"] == 50  # 5 perguntas * 10 pontos
    assert finish_data["correct_answers"] == 5
    assert finish_data["total_questions"] == 5
    assert finish_data["accuracy"] == 100.0
    
    # 4. Verificar histórico
    response = client.get(
        "/api/quiz/history",
        headers=auth_headers
    )
    assert response.status_code == 200
    history_data = response.json()
    assert history_data["total_quizzes"] == 1
    assert len(history_data["quizzes"]) == 1
    assert history_data["quizzes"][0]["quiz_id"] == quiz_id
    assert history_data["quizzes"][0]["final_score"] == 50

def test_quiz_with_mixed_answers(client, db_session, auth_headers):
    """Teste E2E: Quiz com respostas corretas e incorretas"""
    
    # Adicionar perguntas
    questions_data = [
        {"correct": "A", "text": "Pergunta 1?"},
        {"correct": "B", "text": "Pergunta 2?"},
        {"correct": "C", "text": "Pergunta 3?"},
    ]
    
    for q_data in questions_data:
        q = Question(
            text=q_data["text"],
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer=q_data["correct"],
            explanation="Explicação"
        )
        db_session.add(q)
    db_session.commit()
    
    # Iniciar quiz
    response = client.post(
        "/api/quiz/start",
        json={"num_questions": 3},
        headers=auth_headers
    )
    quiz_id = response.json()["quiz_id"]
    questions = response.json()["questions"]
    
    # Responder: correta, incorreta, correta
    answers = ["A", "A", "C"]  # Segunda resposta está errada (deveria ser B)
    
    for i, question in enumerate(questions):
        response = client.post(
            f"/api/quiz/{quiz_id}/answer",
            json={
                "question_id": question["id"],
                "answer": answers[i],
                "time_taken": 2.5
            },
            headers=auth_headers
        )
        assert response.status_code == 200
    
    # Finalizar
    response = client.post(
        f"/api/quiz/{quiz_id}/finish",
        headers=auth_headers
    )
    finish_data = response.json()
    
    assert finish_data["final_score"] == 20  # 2 corretas * 10
    assert finish_data["correct_answers"] == 2
    assert finish_data["incorrect_answers"] == 1
    assert finish_data["accuracy"] == pytest.approx(66.7, abs=0.1)

