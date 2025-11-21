import pytest
from app.services.quiz_service import QuizService
from app.models.user import User
from app.models.question import Question
from app.models.quiz import QuizSession
from app.models.answer import Answer
from fastapi import HTTPException

class TestQuizServiceGetRandomQuestions:
    """Testes para busca de perguntas aleatórias"""
    
    def test_get_random_questions_without_filters(self, db_session):
        """Teste: Buscar perguntas sem filtros"""
        # Criar perguntas
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
        
        questions = QuizService.get_random_questions(db_session, 5, None, None)
        
        assert len(questions) == 5
    
    def test_get_random_questions_with_category_filter(self, db_session):
        """Teste: Buscar perguntas com filtro de categoria"""
        # Criar perguntas de diferentes categorias
        for i in range(5):
            q = Question(
                text=f"Geografia {i}?",
                category="geografia",
                difficulty="facil",
                question_type="multiple_choice",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Explicação"
            )
            db_session.add(q)
        
        for i in range(5):
            q = Question(
                text=f"Historia {i}?",
                category="historia",
                difficulty="facil",
                question_type="multiple_choice",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Explicação"
            )
            db_session.add(q)
        db_session.commit()
        
        questions = QuizService.get_random_questions(db_session, 3, "geografia", None)
        
        assert len(questions) == 3
        assert all(q.category == "geografia" for q in questions)
    
    def test_get_random_questions_with_difficulty_filter(self, db_session):
        """Teste: Buscar perguntas com filtro de dificuldade"""
        for i in range(5):
            q = Question(
                text=f"Facil {i}?",
                category="geral",
                difficulty="facil",
                question_type="multiple_choice",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Explicação"
            )
            db_session.add(q)
        db_session.commit()
        
        questions = QuizService.get_random_questions(db_session, 3, None, "facil")
        
        assert len(questions) == 3
        assert all(q.difficulty == "facil" for q in questions)
    
    def test_get_random_questions_insufficient_questions(self, db_session):
        """Teste: Erro quando não há perguntas suficientes"""
        # Criar apenas 2 perguntas
        for i in range(2):
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
        
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_random_questions(db_session, 5, None, None)
        
        assert exc_info.value.status_code == 400
        assert "não há perguntas suficientes" in exc_info.value.detail.lower()
    
    def test_get_random_questions_invalid_category(self, db_session):
        """Teste: Erro com categoria inválida"""
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_random_questions(db_session, 5, "invalid_category", None)
        
        assert exc_info.value.status_code == 400
    
    def test_get_random_questions_invalid_difficulty(self, db_session):
        """Teste: Erro com dificuldade inválida"""
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_random_questions(db_session, 5, None, "invalid_difficulty")
        
        assert exc_info.value.status_code == 400

class TestQuizServiceRecordAnswer:
    """Testes para registro de respostas"""
    
    def test_record_answer_correct(self, db_session):
        """Teste: Registrar resposta correta"""
        # Criar usuário e quiz
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        question = Question(
            text="Pergunta?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(question)
        db_session.commit()
        
        is_correct, q = QuizService.record_answer(db_session, quiz, question.id, "A", 3.0)
        
        assert is_correct == True
        assert q.id == question.id
        
        # Verificar se resposta foi salva
        answer = db_session.query(Answer).filter(Answer.quiz_session_id == quiz.id).first()
        assert answer is not None
        assert answer.is_correct == True
    
    def test_record_answer_incorrect(self, db_session):
        """Teste: Registrar resposta incorreta"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        question = Question(
            text="Pergunta?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(question)
        db_session.commit()
        
        is_correct, q = QuizService.record_answer(db_session, quiz, question.id, "B", 5.0)
        
        assert is_correct == False
    
    def test_record_answer_duplicate(self, db_session):
        """Teste: Erro ao responder pergunta duplicada"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        question = Question(
            text="Pergunta?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(question)
        db_session.commit()
        
        # Primeira resposta
        QuizService.record_answer(db_session, quiz, question.id, "A", 3.0)
        
        # Tentar responder novamente
        with pytest.raises(HTTPException) as exc_info:
            QuizService.record_answer(db_session, quiz, question.id, "B", 2.0)
        
        assert exc_info.value.status_code == 400
        assert "já foi respondida" in exc_info.value.detail.lower()
    
    def test_record_answer_completed_quiz(self, db_session):
        """Teste: Erro ao responder quiz já finalizado"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(
            user_id=user.id,
            total_questions=5,
            category=None,
            difficulty=None,
            is_completed=True
        )
        db_session.add(quiz)
        db_session.commit()
        
        question = Question(
            text="Pergunta?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(question)
        db_session.commit()
        
        with pytest.raises(HTTPException) as exc_info:
            QuizService.record_answer(db_session, quiz, question.id, "A", 3.0)
        
        assert exc_info.value.status_code == 400
        assert "já foi finalizado" in exc_info.value.detail.lower()

class TestQuizServiceGetQuizSession:
    """Testes para busca de sessão de quiz"""
    
    def test_get_quiz_session_valid(self, db_session):
        """Teste: Buscar sessão de quiz válida"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        found_quiz = QuizService.get_quiz_session(db_session, quiz.id, user.id)
        
        assert found_quiz.id == quiz.id
        assert found_quiz.user_id == user.id
    
    def test_get_quiz_session_not_found(self, db_session):
        """Teste: Erro quando quiz não existe"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_quiz_session(db_session, 999, user.id)
        
        assert exc_info.value.status_code == 404
    
    def test_get_quiz_session_wrong_user(self, db_session):
        """Teste: Erro quando quiz pertence a outro usuário"""
        user1 = User(username="user1", email="user1@test.com", password_hash="hash")
        user2 = User(username="user2", email="user2@test.com", password_hash="hash")
        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()
        
        quiz = QuizSession(user_id=user1.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_quiz_session(db_session, quiz.id, user2.id)
        
        assert exc_info.value.status_code == 403

class TestQuizServiceGetQuizProgress:
    """Testes para progresso do quiz"""
    
    def test_get_quiz_progress_no_answers(self, db_session):
        """Teste: Progresso sem respostas"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        progress = QuizService.get_quiz_progress(db_session, quiz)
        
        assert progress["questions_answered"] == 0
        assert progress["questions_remaining"] == 5
        assert progress["correct_answers"] == 0
        assert progress["current_score"] == 0
        assert progress["has_next_question"] == True
    
    def test_get_quiz_progress_with_answers(self, db_session):
        """Teste: Progresso com respostas"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        question = Question(
            text="Pergunta?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(question)
        db_session.commit()
        
        # Registrar 2 respostas corretas
        QuizService.record_answer(db_session, quiz, question.id, "A", 3.0)
        
        # Criar segunda pergunta e resposta
        question2 = Question(
            text="Pergunta 2?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="B",
            explanation="Explicação"
        )
        db_session.add(question2)
        db_session.commit()
        
        QuizService.record_answer(db_session, quiz, question2.id, "B", 2.0)
        
        progress = QuizService.get_quiz_progress(db_session, quiz)
        
        assert progress["questions_answered"] == 2
        assert progress["questions_remaining"] == 3
        assert progress["correct_answers"] == 2
        assert progress["current_score"] == 20
        assert progress["has_next_question"] == True

