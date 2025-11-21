import pytest
from fastapi import HTTPException
from app.services.quiz_service import QuizService
from app.models.user import User
from app.models.question import Question
from app.models.quiz import QuizSession


def test_get_random_questions_returns_correct_amount(db_session):
    """Teste unitário: get_random_questions retorna quantidade solicitada"""
    # Adicionar 10 perguntas
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
    
    # Solicitar 5
    questions = QuizService.get_random_questions(db_session, 5, None, None)
    
    assert len(questions) == 5


def test_get_random_questions_filters_by_category(db_session):
    """Teste unitário: get_random_questions filtra por categoria"""
    # Adicionar perguntas de diferentes categorias
    for i in range(5):
        db_session.add(Question(
            text=f"Geografia {i}?",
            category="geografia",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Ex"
        ))
    
    for i in range(5):
        db_session.add(Question(
            text=f"Historia {i}?",
            category="historia",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Ex"
        ))
    db_session.commit()
    
    # Buscar apenas geografia
    questions = QuizService.get_random_questions(db_session, 3, "geografia", None)
    
    assert len(questions) == 3
    assert all(q.category == "geografia" for q in questions)


def test_get_random_questions_filters_by_difficulty(db_session):
    """Teste unitário: get_random_questions filtra por dificuldade"""
    for i in range(3):
        db_session.add(Question(
            text=f"Facil {i}?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Ex"
        ))
    
    for i in range(3):
        db_session.add(Question(
            text=f"Dificil {i}?",
            category="geral",
            difficulty="dificil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Ex"
        ))
    db_session.commit()
    
    questions = QuizService.get_random_questions(db_session, 2, None, "facil")
    
    assert len(questions) == 2
    assert all(q.difficulty == "facil" for q in questions)


def test_create_quiz_session_creates_successfully(db_session):
    """Teste unitário: create_quiz_session cria sessão"""
    user = User(username="test", email="test@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    quiz = QuizService.create_quiz_session(
        db_session,
        user.id,
        "geografia",
        "facil",
        5
    )
    
    assert quiz.id is not None
    assert quiz.user_id == user.id
    assert quiz.category == "geografia"
    assert quiz.difficulty == "facil"
    assert quiz.total_questions == 5


def test_quiz_session_has_started_at_timestamp(db_session):
    """Teste unitário: quiz criado tem timestamp de início"""
    user = User(username="test", email="test@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
    
    assert quiz.started_at is not None


def test_get_quiz_session_from_database(db_session):
    """Teste unitário: quiz criado pode ser recuperado do banco"""
    user = User(username="test", email="test@test.com", password_hash="hash")
    db_session.add(user)
    db_session.commit()
    
    # Criar quiz
    quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
    quiz_id = quiz.id
    
    # Buscar no banco
    found_quiz = db_session.query(QuizSession).filter(QuizSession.id == quiz_id).first()
    
    assert found_quiz is not None
    assert found_quiz.id == quiz_id
    assert found_quiz.user_id == user.id
