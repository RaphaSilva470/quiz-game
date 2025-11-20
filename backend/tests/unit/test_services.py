import pytest
from app.services.auth_service import AuthService
from app.services.quiz_service import QuizService
from app.models.user import User
from app.models.question import Question
from app.schemas.auth import UserRegister

def test_user_exists(db_session):
    """Teste: Verificar se usuário existe"""
    # Criar usuário
    user = User(
        username="test",
        email="test@test.com",
        password_hash="hash123"
    )
    db_session.add(user)
    db_session.commit()
    
    # Verificar
    assert AuthService.user_exists(db_session, "test@test.com") == True
    assert AuthService.user_exists(db_session, "naoexiste@test.com") == False

def test_username_exists(db_session):
    """Teste: Verificar se username existe"""
    user = User(
        username="joao",
        email="joao@test.com",
        password_hash="hash123"
    )
    db_session.add(user)
    db_session.commit()
    
    assert AuthService.username_exists(db_session, "joao") == True
    assert AuthService.username_exists(db_session, "maria") == False

def test_create_user(db_session):
    """Teste: Criar usuário"""
    user_data = UserRegister(
        username="newuser",
        email="new@test.com",
        password="senha123"
    )
    
    user = AuthService.create_user(db_session, user_data)
    
    assert user.id is not None
    assert user.username == "newuser"
    assert user.email == "new@test.com"
    assert user.password_hash != "senha123"

def test_get_random_questions(db_session):
    """Teste: Buscar perguntas aleatórias"""
    # Adicionar perguntas
    for i in range(10):
        q = Question(
            text=f"Pergunta {i}?",
            category="geografia",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(q)
    db_session.commit()
    
    # Buscar 5 aleatórias
    questions = QuizService.get_random_questions(db_session, 5, None, None)
    
    assert len(questions) == 5
    assert all(q.category == "geografia" for q in questions)

def test_create_quiz_session(db_session):
    """Teste: Criar sessão de quiz"""
    # Criar usuário
    user = User(
        username="test",
        email="test@test.com",
        password_hash="hash"
    )
    db_session.add(user)
    db_session.commit()
    
    # Criar sessão
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
    assert quiz.total_questions == 5