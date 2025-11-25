# Sistema de Jogo de Quiz

## 1. Membros do Grupo
- Raphaela Maria Costa e Silva  
- Eduardo Klausing Gervasio Muniz  

## 2. Explicação do Sistema
O sistema consiste em um **jogo de quiz**, onde os usuários respondem a perguntas de múltipla escolha ou verdadeiro/falso. O objetivo principal é testar e estimular o conhecimento dos jogadores em diferentes categorias, promovendo aprendizado de forma interativa e divertida.  

O sistema é projetado para ser **intuitivo e dinâmico**, oferecendo feedback imediato sobre cada resposta e mantendo o engajamento do usuário. Ele também permite acompanhar o desempenho ao longo do tempo, promovendo competitividade saudável entre os participantes.  

Funcionalidades principais incluem:  
- **Registro de usuários:** Permite que os jogadores criem contas, salvem seu progresso e personalizem seu perfil.  
- **Diferentes níveis de dificuldade:** As perguntas podem ser classificadas como fáceis, médias ou difíceis, permitindo que o sistema se adapte ao nível de conhecimento do jogador.  
- **Temporizador para cada pergunta:** Cria um desafio adicional e ajuda a manter o ritmo do jogo.  
- **Histórico de pontuação e ranking:** Permite que os usuários vejam seu desempenho anterior e comparem suas pontuações com outros jogadores, estimulando a competitividade.  
- **Categorias variadas de perguntas:** Possibilidade de escolher entre diferentes temas, como ciência, história, esportes ou cultura geral, tornando o jogo mais diversificado e educativo.  
- **Feedback imediato:** Ao responder, o jogador recebe confirmação se a resposta está correta ou não, com explicações opcionais para aprendizado adicional.  
- **Sistema de pontuação progressivo:** Recompensa acertos consecutivos ou respostas rápidas com pontos adicionais, tornando o jogo mais envolvente.  

O objetivo final do sistema é combinar entretenimento e aprendizado, oferecendo uma experiência divertida, educativa e competitiva para os usuários.
 

## 3. Tecnologias Utilizadas
- **Front-end:** React  
- **Back-end:** FastAPI (Python 3.13) , Uvicorn, SQLAlchemy, SQLite, Passlib + Argon2, Pydantic, Python-JOSE, Pytest

## 4.Como Rodar o Backend

### 4.1. Configurar o ambiente
Clone o repositório e entre na pasta do backend:

```bash
cd quiz_game/backend
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
python scripts/init_db.py 
python scripts/seed_questions.py
uvicorn app.main:app --reload
```
### 4.2 Configurar o frontend
(Abra outro terminal)
```bash
cd frontend
npm install
npm start
```
### 5. Como rodar os testes localmente
Dentro de quiz-game/backend rode:

```bash
python -m pytest tests/ --cov=app --cov-report=term
```
