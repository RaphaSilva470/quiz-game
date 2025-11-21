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


class TestGetQuizSession:
    """Testes para QuizService.get_quiz_session"""
    
    def test_should_return_quiz_when_exists_and_belongs_to_user(self, db_session, user):
        """Deve retornar quiz quando existe e pertence ao usuário"""
        quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
        
        found_quiz = QuizService.get_quiz_session(db_session, quiz.id, user.id)
        
        assert found_quiz is not None
        assert found_quiz.id == quiz.id
        assert found_quiz.user_id == user.id
    
    def test_should_raise_exception_when_quiz_not_found(self, db_session, user):
        """Deve lançar exceção quando quiz não existe"""
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_quiz_session(db_session, 99999, user.id)
        
        assert exc_info.value.status_code == 404
        assert "não encontrado" in exc_info.value.detail.lower()
    
    def test_should_raise_exception_when_quiz_belongs_to_other_user(self, db_session, user):
        """Deve lançar exceção quando quiz pertence a outro usuário"""
        other_user = User(
            username="other",
            email="other@test.com",
            password_hash="hash"
        )
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)
        
        quiz = QuizService.create_quiz_session(db_session, other_user.id, "geral", "facil", 5)
        
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_quiz_session(db_session, quiz.id, user.id)
        
        assert exc_info.value.status_code == 403
        assert "acesso negado" in exc_info.value.detail.lower()


class TestRecordAnswer:
    """Testes para QuizService.record_answer"""
    
    def test_should_record_correct_answer(self, db_session, user):
        """Deve registrar resposta correta"""
        quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
        
        question = Question(
            text="Teste?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Teste"
        )
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        is_correct, returned_question = QuizService.record_answer(
            db_session, quiz, question.id, "A", 5.0
        )
        
        assert is_correct is True
        assert returned_question.id == question.id
        
        from app.models.answer import Answer
        answer = db_session.query(Answer).filter(
            Answer.quiz_session_id == quiz.id,
            Answer.question_id == question.id
        ).first()
        assert answer is not None
        assert answer.is_correct is True
    
    def test_should_record_incorrect_answer(self, db_session, user):
        """Deve registrar resposta incorreta"""
        quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
        
        question = Question(
            text="Teste?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Teste"
        )
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        is_correct, returned_question = QuizService.record_answer(
            db_session, quiz, question.id, "B", 5.0
        )
        
        assert is_correct is False
        assert returned_question.id == question.id
        
        from app.models.answer import Answer
        answer = db_session.query(Answer).filter(
            Answer.quiz_session_id == quiz.id,
            Answer.question_id == question.id
        ).first()
        assert answer is not None
        assert answer.is_correct is False


class TestGetQuizProgress:
    """Testes para QuizService.get_quiz_progress"""
    
    def test_should_return_correct_progress(self, db_session, user):
        """Deve retornar progresso correto do quiz"""
        quiz = QuizService.create_quiz_session(db_session, user.id, "geral", "facil", 5)
        
        question1 = Question(
            text="Pergunta 1?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Teste"
        )
        question2 = Question(
            text="Pergunta 2?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="B",
            explanation="Teste"
        )
        db_session.add(question1)
        db_session.add(question2)
        db_session.commit()
        db_session.refresh(question1)
        db_session.refresh(question2)
        
        # Responder 2 perguntas (1 correta, 1 incorreta)
        QuizService.record_answer(db_session, quiz, question1.id, "A", 3.0)
        QuizService.record_answer(db_session, quiz, question2.id, "A", 4.0)
        
        progress = QuizService.get_quiz_progress(db_session, quiz)
        
        assert progress["questions_answered"] == 2
        assert progress["questions_remaining"] == 3
        assert progress["correct_answers"] == 1
        assert progress["current_score"] == 10
        assert progress["has_next_question"] is True