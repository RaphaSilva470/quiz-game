import pytest
from app.services.score_service import ScoreService
from app.models.user import User
from app.models.quiz import QuizSession
from app.models.question import Question
from app.models.answer import Answer
from app.models.score import Score
from fastapi import HTTPException

class TestScoreServiceCalculateAndSave:
    """Testes para cálculo e salvamento de pontuação"""
    
    def test_calculate_score_all_correct(self, db_session):
        """Teste: Calcular pontuação com todas corretas"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=3, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        # Criar perguntas e respostas corretas
        for i in range(3):
            question = Question(
                text=f"Pergunta {i}?",
                category="geral",
                difficulty="facil",
                question_type="multiple_choice",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Explicação"
            )
            db_session.add(question)
            db_session.commit()
            
            answer = Answer(
                quiz_session_id=quiz.id,
                question_id=question.id,
                user_answer="A",
                is_correct=True,
                time_taken=3.0
            )
            db_session.add(answer)
        db_session.commit()
        
        score = ScoreService.calculate_and_save_score(db_session, quiz)
        
        assert score.total_score == 30
        assert score.correct_answers == 3
        assert score.total_questions == 3
        assert score.accuracy == 100.0
        assert score.total_time == 9.0
        assert quiz.is_completed == True
    
    def test_calculate_score_mixed(self, db_session):
        """Teste: Calcular pontuação com acertos e erros"""
        user = User(username="test", email="test@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=4, category=None, difficulty=None)
        db_session.add(quiz)
        db_session.commit()
        
        question1 = Question(
            text="Pergunta 1?",
            category="geral",
            difficulty="facil",
            question_type="multiple_choice",
            options=["A", "B", "C", "D"],
            correct_answer="A",
            explanation="Explicação"
        )
        db_session.add(question1)
        db_session.commit()
        
        # Criar mais 3 perguntas para ter 4 no total
        questions = [question1]
        for i in range(3):
            q = Question(
                text=f"Pergunta {i+2}?",
                category="geral",
                difficulty="facil",
                question_type="multiple_choice",
                options=["A", "B", "C", "D"],
                correct_answer="A",
                explanation="Explicação"
            )
            questions.append(q)
            db_session.add(q)
        db_session.commit()
        
        # Adicionar 4 respostas: 2 corretas, 2 incorretas
        db_session.add_all([
            Answer(quiz_session_id=quiz.id, question_id=questions[0].id, user_answer="A", is_correct=True, time_taken=2.0),
            Answer(quiz_session_id=quiz.id, question_id=questions[1].id, user_answer="B", is_correct=False, time_taken=3.0),
            Answer(quiz_session_id=quiz.id, question_id=questions[2].id, user_answer="A", is_correct=True, time_taken=1.5),
            Answer(quiz_session_id=quiz.id, question_id=questions[3].id, user_answer="C", is_correct=False, time_taken=4.0)
        ])
        db_session.commit()
        
        score = ScoreService.calculate_and_save_score(db_session, quiz)
        
        assert score.correct_answers == 3  # 3 corretas de 4
        assert score.total_questions == 4
        assert score.total_score == 30
        assert score.accuracy == 75.0

class TestScoreServiceGetGlobalRanking:
    """Testes para ranking global"""
    
    def test_get_global_ranking_single_user(self, db_session):
        """Teste: Ranking com um usuário"""
        user = User(username="user1", email="user1@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, category=None, difficulty=None, is_completed=True)
        db_session.add(quiz)
        db_session.commit()
        
        score = Score(
            user_id=user.id,
            quiz_session_id=quiz.id,
            total_score=50,
            correct_answers=5,
            total_questions=5,
            accuracy=100.0,
            total_time=15.0
        )
        db_session.add(score)
        db_session.commit()
        
        ranking = ScoreService.get_global_ranking(db_session, limit=10)
        
        assert len(ranking) == 1
        assert ranking[0]["username"] == "user1"
        assert ranking[0]["total_score"] == 50
        assert ranking[0]["position"] == 1
    
    def test_get_global_ranking_multiple_users(self, db_session):
        """Teste: Ranking com múltiplos usuários ordenados"""
        # Criar 3 usuários
        users = []
        for i in range(3):
            user = User(username=f"user{i}", email=f"user{i}@test.com", password_hash="hash")
            users.append(user)
            db_session.add(user)
        db_session.commit()
        
        # Criar quizzes e scores
        # User 0: 100 pontos
        quiz0 = QuizSession(user_id=users[0].id, total_questions=10, is_completed=True)
        db_session.add(quiz0)
        db_session.commit()
        score0 = Score(user_id=users[0].id, quiz_session_id=quiz0.id, total_score=100, correct_answers=10, total_questions=10, accuracy=100.0, total_time=30.0)
        db_session.add(score0)
        
        # User 1: 50 pontos
        quiz1 = QuizSession(user_id=users[1].id, total_questions=5, is_completed=True)
        db_session.add(quiz1)
        db_session.commit()
        score1 = Score(user_id=users[1].id, quiz_session_id=quiz1.id, total_score=50, correct_answers=5, total_questions=5, accuracy=100.0, total_time=20.0)
        db_session.add(score1)
        
        # User 2: 75 pontos
        quiz2 = QuizSession(user_id=users[2].id, total_questions=8, is_completed=True)
        db_session.add(quiz2)
        db_session.commit()
        score2 = Score(user_id=users[2].id, quiz_session_id=quiz2.id, total_score=75, correct_answers=8, total_questions=8, accuracy=100.0, total_time=25.0)
        db_session.add(score2)
        
        db_session.commit()
        
        ranking = ScoreService.get_global_ranking(db_session, limit=10)
        
        assert len(ranking) == 3
        assert ranking[0]["username"] == "user0"  # Maior pontuação
        assert ranking[0]["total_score"] == 100
        assert ranking[1]["username"] == "user2"  # Segunda maior
        assert ranking[2]["username"] == "user1"  # Menor pontuação

class TestScoreServiceGetUserPosition:
    """Testes para posição do usuário no ranking"""
    
    def test_get_user_position_first(self, db_session):
        """Teste: Usuário em primeiro lugar"""
        user = User(username="user1", email="user1@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, is_completed=True)
        db_session.add(quiz)
        db_session.commit()
        
        score = Score(user_id=user.id, quiz_session_id=quiz.id, total_score=100, correct_answers=5, total_questions=5, accuracy=100.0, total_time=20.0)
        db_session.add(score)
        db_session.commit()
        
        position = ScoreService.get_user_position(db_session, user.id)
        
        assert position == 1
    
    def test_get_user_position_with_others(self, db_session):
        """Teste: Posição do usuário com outros no ranking"""
        users = []
        for i in range(3):
            user = User(username=f"user{i}", email=f"user{i}@test.com", password_hash="hash")
            users.append(user)
            db_session.add(user)
        db_session.commit()
        
        # User 0: 100 pontos
        quiz0 = QuizSession(user_id=users[0].id, total_questions=10, is_completed=True)
        db_session.add(quiz0)
        db_session.commit()
        score0 = Score(user_id=users[0].id, quiz_session_id=quiz0.id, total_score=100, correct_answers=10, total_questions=10, accuracy=100.0, total_time=30.0)
        db_session.add(score0)
        
        # User 1: 50 pontos (usuário testado)
        quiz1 = QuizSession(user_id=users[1].id, total_questions=5, is_completed=True)
        db_session.add(quiz1)
        db_session.commit()
        score1 = Score(user_id=users[1].id, quiz_session_id=quiz1.id, total_score=50, correct_answers=5, total_questions=5, accuracy=100.0, total_time=20.0)
        db_session.add(score1)
        
        # User 2: 75 pontos
        quiz2 = QuizSession(user_id=users[2].id, total_questions=8, is_completed=True)
        db_session.add(quiz2)
        db_session.commit()
        score2 = Score(user_id=users[2].id, quiz_session_id=quiz2.id, total_score=75, correct_answers=8, total_questions=8, accuracy=100.0, total_time=25.0)
        db_session.add(score2)
        
        db_session.commit()
        
        position = ScoreService.get_user_position(db_session, users[1].id)
        
        assert position == 3  # Terceiro lugar (100, 75, 50)

class TestScoreServiceGetUserStats:
    """Testes para estatísticas do usuário"""
    
    def test_get_user_stats_no_scores(self, db_session):
        """Teste: Estatísticas de usuário sem scores"""
        user = User(username="user1", email="user1@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        stats = ScoreService.get_user_stats(db_session, user.id)
        
        assert stats["user_id"] == user.id
        assert stats["username"] == "user1"
        assert stats["overall"]["total_quizzes"] == 0
        assert stats["overall"]["total_score"] == 0
    
    def test_get_user_stats_with_scores(self, db_session):
        """Teste: Estatísticas de usuário com scores"""
        user = User(username="user1", email="user1@test.com", password_hash="hash")
        db_session.add(user)
        db_session.commit()
        
        quiz = QuizSession(user_id=user.id, total_questions=5, is_completed=True)
        db_session.add(quiz)
        db_session.commit()
        
        score = Score(user_id=user.id, quiz_session_id=quiz.id, total_score=50, correct_answers=5, total_questions=5, accuracy=100.0, total_time=20.0)
        db_session.add(score)
        db_session.commit()
        
        stats = ScoreService.get_user_stats(db_session, user.id)
        
        assert stats["overall"]["total_quizzes"] == 1
        assert stats["overall"]["total_score"] == 50
        assert stats["overall"]["correct_answers"] == 5
        assert stats["overall"]["accuracy"] == 100.0
    
    def test_get_user_stats_user_not_found(self, db_session):
        """Teste: Erro quando usuário não existe"""
        with pytest.raises(HTTPException) as exc_info:
            ScoreService.get_user_stats(db_session, 999)
        
        assert exc_info.value.status_code == 404

