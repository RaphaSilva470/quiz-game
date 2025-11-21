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
    return questions


class TestQuizFlow:
    """Testes de integração para fluxo completo de quiz"""
    
    def test_should_complete_full_quiz_workflow(
        self, client, auth_headers, quiz_questions
    ):
        """Fluxo completo: iniciar → responder → finalizar → verificar histórico e ranking"""
        
        start_response = client.post(
            "/api/quiz/start",
            json={"num_questions": 5},
            headers=auth_headers
        )
        assert start_response.status_code == 201
        
        quiz_data = start_response.json()
        quiz_id = quiz_data["quiz_id"]
        questions = quiz_data["questions"]
        
        assert len(questions) == 5
        assert "id" in questions[0]
        
        for question in questions:
            answer_response = client.post(
                f"/api/quiz/{quiz_id}/answer",
                json={
                    "question_id": question["id"],
                    "answer": "A",
                    "time_taken": 5.0
                },
                headers=auth_headers
            )
            
            assert answer_response.status_code == 200
            answer_data = answer_response.json()
            assert answer_data["is_correct"] is True
        
        finish_response = client.post(
            f"/api/quiz/{quiz_id}/finish",
            headers=auth_headers
        )
        assert finish_response.status_code == 200
        
        result = finish_response.json()
        assert result["correct_answers"] == 5
        assert result["final_score"] == 50
        assert result["accuracy"] == 100.0
        
        history_response = client.get("/api/quiz/history", headers=auth_headers)
        assert history_response.status_code == 200
        
        history = history_response.json()
        assert history["total_quizzes"] == 1
        
        ranking_response = client.get("/api/ranking/global", headers=auth_headers)
        assert ranking_response.status_code == 200
        
        ranking = ranking_response.json()
        assert len(ranking["ranking"]) > 0