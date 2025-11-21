import pytest
from app.models.question import Question
from app.models.quiz import QuizSession
from app.models.score import Score


@pytest.fixture
def stats_questions(db_session):
    """Fixture: cria perguntas para testes de estatísticas"""
    for i in range(20):
        q = Question(
            text=f"Pergunta {i}?",
            category="geografia" if i % 2 == 0 else "historia",
            difficulty="facil" if i < 10 else "medio",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(q)
    db_session.commit()


def test_user_stats_after_multiple_quizzes(client, db_session, auth_headers, stats_questions):
    """Teste de integração: Estatísticas do usuário após múltiplos quizzes"""
    
    from app.services.auth_service import AuthService
    user = AuthService.get_user_by_email(db_session, "test@test.com")
    
    # Criar 2 quizzes completos
    for quiz_num in range(2):
        response = client.post(
            "/api/quiz/start",
            json={"num_questions": 5, "category": "geografia", "difficulty": "facil"},
            headers=auth_headers
        )
        quiz_id = response.json()["quiz_id"]
        questions = response.json()["questions"]
        
        # Responder todas corretas
        for question in questions:
            client.post(
                f"/api/quiz/{quiz_id}/answer",
                json={
                    "question_id": question["id"],
                    "answer": "A",
                    "time_taken": 3.0
                },
                headers=auth_headers
            )
        
        client.post(f"/api/quiz/{quiz_id}/finish", headers=auth_headers)
    
    # Verificar estatísticas no banco
    completed_quizzes = db_session.query(QuizSession).filter(
        QuizSession.user_id == user.id,
        QuizSession.is_completed == True
    ).count()
    
    assert completed_quizzes == 2
    
    scores = db_session.query(Score).filter(Score.user_id == user.id).all()
    assert len(scores) == 2
    assert all(s.total_score == 50 for s in scores)  # 5 perguntas * 10 pontos cada
