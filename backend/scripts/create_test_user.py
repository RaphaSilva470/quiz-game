"""
Script para criar um usuário de teste
"""
import sys
import os

# na raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password

def create_test_user():
    db = SessionLocal()
    try:
        # Verificar se o usuário já existe
        existing_user = db.query(User).filter(User.email == "teste@teste.com").first()
        if existing_user:
            print("Usuário de teste já existe!")
            print(f"Email: teste@teste.com")
            print(f"Senha: teste123")
            print(f"Username: {existing_user.username}")
            return
        
        # Criar novo usuário
        test_user = User(
            username="teste",
            email="teste@teste.com",
            password_hash=hash_password("teste123")
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("=" * 50)
        print("Usuário de teste criado com sucesso!")
        print("=" * 50)
        print(f"Email: teste@teste.com")
        print(f"Senha: teste123")
        print(f"Username: teste")
        print("=" * 50)
        
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar usuário: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()

