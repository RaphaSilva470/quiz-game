import pytest
from fastapi import HTTPException
from app.services.quiz_service import QuizService
from app.models.user import User
from app.models.question import Question
from app.models.quiz import QuizSession


@pytest.fixture
def user(db_session):
    """Fixture: cria um usuário no banco de dados"""
    user = User(
        username="test",
        email="test@test.com",
        password_hash="hash"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_questions(db_session):
    """Fixture: cria perguntas de exemplo no banco"""
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
def questions_by_category(db_session):
    """Fixture: cria perguntas de diferentes categorias"""
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


@pytest.fixture
def questions_by_difficulty(db_session):
    """Fixture: cria perguntas de diferentes dificuldades"""
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


class TestGetRandomQuestions:
    """Testes para QuizService.get_random_questions"""
    
    def test_should_return_requested_amount(self, db_session, sample_questions):
        questions = QuizService.get_random_questions(db_session, 5, None, None)
        assert len(questions) == 5
    
    def test_should_filter_by_category(self, db_session, questions_by_category):
        questions = QuizService.get_random_questions(db_session, 3, "geografia", None)
        
        assert len(questions) == 3
        assert all(q.category == "geografia" for q in questions)
    
    def test_should_filter_by_difficulty(self, db_session, questions_by_difficulty):
        questions = QuizService.get_random_questions(db_session, 2, None, "facil")
        
        assert len(questions) == 2
        assert all(q.difficulty == "facil" for q in questions)


class TestCreateQuizSession:
    """Testes para QuizService.create_quiz_session"""
    
    def test_should_create_session_successfully(self, db_session, user):
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
    
    def test_should_have_started_at_timestamp(self, db_session, user):
        quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
        assert quiz.started_at is not None
    
    def test_should_be_retrievable_from_database(self, db_session, user):
        quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
        quiz_id = quiz.id
        
        found_quiz = db_session.query(QuizSession).filter(QuizSession.id == quiz_id).first()
        
        assert found_quiz is not None
        assert found_quiz.id == quiz_id
        assert found_quiz.user_id == user.id