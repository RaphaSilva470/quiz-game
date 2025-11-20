"""
criar tabelas banco de dados
"""
import sys
import os

# na raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models import User, Question, QuizSession, Answer, Score

def init_db():    
    Base.metadata.create_all(bind=engine)
    
    print("Tabelas criadas com sucesso!")
    print("Tabelas criadas:")
    print(" users")
    print("questions")
    print("quiz_sessions")
    print("answers")
    print("scores")

if __name__ == "__main__":
    init_db()