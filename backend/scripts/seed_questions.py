import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.question import Question

def seed_questions():
    """Adiciona perguntas de exemplo ao banco"""
    db = SessionLocal()
    
    # Verificar se já tem perguntas
    existing = db.query(Question).first()
    if existing:
        print("Banco já contém perguntas!")
        response = input("Deseja adicionar mais perguntas? (s/n): ")
        if response.lower() != 's':
            print("Cancelado.")
            return
    
    questions = [
        # GEOGRAFIA - FÁCIL
        {
            "text": "Qual é a capital do Brasil?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
            "correct_answer": "Brasília",
            "explanation": "Brasília foi inaugurada em 21 de abril de 1960 como a nova capital federal do Brasil."
        },
        {
            "text": "Qual é o maior país do mundo em área territorial?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Canadá", "China", "Estados Unidos", "Rússia"],
            "correct_answer": "Rússia",
            "explanation": "A Rússia possui aproximadamente 17 milhões de km², sendo o maior país do mundo."
        },
        {
            "text": "Qual oceano banha a costa leste do Brasil?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Oceano Pacífico", "Oceano Atlântico", "Oceano Índico", "Oceano Ártico"],
            "correct_answer": "Oceano Atlântico",
            "explanation": "O Oceano Atlântico banha toda a costa leste brasileira."
        },
        {
            "text": "Qual o maior oceano do mundo?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Atlântico", "Índico", "Pacífico", "Ártico"],
            "correct_answer": "Pacífico",
            "explanation": "O Oceano Pacífico é o maior oceano, cobrindo cerca de 165 milhões de km²."
        },
        {
            "text": "Quantos continentes existem no mundo?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["5", "6", "7", "8"],
            "correct_answer": "7",
            "explanation": "Os 7 continentes são: África, Américas (Norte e Sul), Antártida, Ásia, Europa e Oceania."
        },
        {
            "text": "Qual o rio mais extenso do Brasil?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Rio São Francisco", "Rio Paraná", "Rio Amazonas", "Rio Tietê"],
            "correct_answer": "Rio Amazonas",
            "explanation": "O Rio Amazonas é o mais extenso do Brasil, com cerca de 6.992 km."
        },
        {
            "text": "Qual país tem a maior população do mundo?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Estados Unidos", "Índia", "China", "Indonésia"],
            "correct_answer": "China",
            "explanation": "A China é o país mais populoso do mundo, com mais de 1,4 bilhão de habitantes."
        },
        
        # GEOGRAFIA - MÉDIO
        {
            "text": "Qual é a capital da Austrália?",
            "category": "geografia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
            "correct_answer": "Canberra",
            "explanation": "Canberra é a capital da Austrália, escolhida como compromisso entre Sydney e Melbourne."
        },
        {
            "text": "Qual o rio mais extenso do mundo?",
            "category": "geografia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Rio Nilo", "Rio Amazonas", "Rio Yangtzé", "Rio Mississippi"],
            "correct_answer": "Rio Amazonas",
            "explanation": "O Rio Amazonas possui cerca de 6.992 km de extensão, sendo o mais longo do mundo."
        },
        
        # GEOGRAFIA - DIFÍCIL
        {
            "text": "Qual é o menor país do mundo?",
            "category": "geografia",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["Mônaco", "San Marino", "Vaticano", "Liechtenstein"],
            "correct_answer": "Vaticano",
            "explanation": "O Vaticano possui apenas 0,44 km² de área, sendo o menor país do mundo."
        },
        
        # HISTÓRIA - FÁCIL
        {
            "text": "Em que ano o Brasil foi descoberto?",
            "category": "historia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["1492", "1500", "1550", "1600"],
            "correct_answer": "1500",
            "explanation": "O Brasil foi descoberto por Pedro Álvares Cabral em 22 de abril de 1500."
        },
        {
            "text": "Quem pintou a Mona Lisa?",
            "category": "historia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Michelangelo", "Leonardo da Vinci", "Rafael", "Donatello"],
            "correct_answer": "Leonardo da Vinci",
            "explanation": "A Mona Lisa foi pintada por Leonardo da Vinci entre 1503 e 1506."
        },
        
        # HISTÓRIA - MÉDIO
        {
            "text": "Em que ano ocorreu a Proclamação da República no Brasil?",
            "category": "historia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["1822", "1889", "1891", "1900"],
            "correct_answer": "1889",
            "explanation": "A Proclamação da República aconteceu em 15 de novembro de 1889."
        },
        {
            "text": "Qual foi a primeira capital do Brasil?",
            "category": "historia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Rio de Janeiro", "Salvador", "São Paulo", "Brasília"],
            "correct_answer": "Salvador",
            "explanation": "Salvador foi a primeira capital do Brasil, de 1549 a 1763."
        },
        
        # CIÊNCIAS - FÁCIL
        {
            "text": "Qual é o planeta mais próximo do Sol?",
            "category": "ciencias",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Vênus", "Terra", "Mercúrio", "Marte"],
            "correct_answer": "Mercúrio",
            "explanation": "Mercúrio é o planeta mais próximo do Sol no Sistema Solar."
        },
        {
            "text": "Quantos ossos tem o corpo humano adulto?",
            "category": "ciencias",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["186", "206", "226", "246"],
            "correct_answer": "206",
            "explanation": "O corpo humano adulto possui 206 ossos."
        },
        
        # CIÊNCIAS - MÉDIO
        {
            "text": "Qual é o maior órgão do corpo humano?",
            "category": "ciencias",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Fígado", "Pulmão", "Pele", "Intestino"],
            "correct_answer": "Pele",
            "explanation": "A pele é o maior órgão do corpo humano, cobrindo toda a superfície corporal."
        },
        
        # ESPORTES - FÁCIL
        {
            "text": "Em que esporte Pelé se destacou?",
            "category": "esportes",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Basquete", "Vôlei", "Futebol", "Tênis"],
            "correct_answer": "Futebol",
            "explanation": "Pelé é considerado um dos maiores jogadores de futebol de todos os tempos."
        },
        {
            "text": "Quantos jogadores tem um time de futebol em campo?",
            "category": "esportes",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["9", "10", "11", "12"],
            "correct_answer": "11",
            "explanation": "Cada time de futebol tem 11 jogadores em campo (10 + goleiro)."
        },
        
        # GERAL - FÁCIL
        {
            "text": "Quantos dias tem um ano?",
            "category": "geral",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["364", "365", "366", "367"],
            "correct_answer": "365",
            "explanation": "Um ano comum tem 365 dias. Anos bissextos têm 366."
        },
        {
            "text": "Qual é a cor do céu em um dia claro?",
            "category": "geral",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Verde", "Azul", "Vermelho", "Amarelo"],
            "correct_answer": "Azul",
            "explanation": "O céu aparenta ser azul devido ao espalhamento da luz solar na atmosfera."
        },
        
        # Adicionar mais 13 perguntas para chegar a 30...
        {
            "text": "O Sol é uma estrela?",
            "category": "ciencias",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Sim", "Não"],
            "correct_answer": "Sim",
            "explanation": "O Sol é uma estrela de tamanho médio, composta principalmente de hidrogênio e hélio."
        },
        {
            "text": "Qual é a velocidade da luz?",
            "category": "ciencias",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["300.000 km/s", "150.000 km/s", "500.000 km/s", "100.000 km/s"],
            "correct_answer": "300.000 km/s",
            "explanation": "A velocidade da luz no vácuo é aproximadamente 300.000 km/s."
        },
        {
            "text": "Quem escreveu 'Dom Casmurro'?",
            "category": "geral",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["José de Alencar", "Machado de Assis", "Graciliano Ramos", "Jorge Amado"],
            "correct_answer": "Machado de Assis",
            "explanation": "Dom Casmurro foi escrito por Machado de Assis em 1899."
        },
        {
            "text": "Qual é a montanha mais alta do mundo?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["K2", "Monte Everest", "Kilimanjaro", "Aconcágua"],
            "correct_answer": "Monte Everest",
            "explanation": "O Monte Everest tem 8.848 metros de altitude, sendo o pico mais alto do mundo."
        },
    ]
    
    print(f"Adicionando {len(questions)} perguntas ao banco...")
    
    for q_data in questions:
        question = Question(**q_data)
        db.add(question)
    
    db.commit()
    print(f"{len(questions)} perguntas adicionadas com sucesso!")
    
    db.close()

if __name__ == "__main__":
    seed_questions()