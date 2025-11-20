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
# ========== MAIS GEOGRAFIA ==========
        
        # GEOGRAFIA - FÁCIL
        {
            "text": "Qual é a capital da França?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Londres", "Paris", "Roma", "Berlim"],
            "correct_answer": "Paris",
            "explanation": "Paris é a capital e maior cidade da França."
        },
        {
            "text": "Em qual continente fica o Brasil?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["África", "Ásia", "América do Sul", "Europa"],
            "correct_answer": "América do Sul",
            "explanation": "O Brasil está localizado na América do Sul."
        },
        {
            "text": "Qual é o deserto mais quente do mundo?",
            "category": "geografia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Saara", "Gobi", "Atacama", "Kalahari"],
            "correct_answer": "Saara",
            "explanation": "O deserto do Saara, na África, é considerado o mais quente do mundo."
        },
        
        # GEOGRAFIA - MÉDIO
        {
            "text": "Qual país tem mais ilhas no mundo?",
            "category": "geografia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Filipinas", "Indonésia", "Suécia", "Noruega"],
            "correct_answer": "Suécia",
            "explanation": "A Suécia possui mais de 220 mil ilhas, sendo o país com mais ilhas do mundo."
        },
        {
            "text": "Qual é a capital do Canadá?",
            "category": "geografia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Toronto", "Vancouver", "Montreal", "Ottawa"],
            "correct_answer": "Ottawa",
            "explanation": "Ottawa é a capital do Canadá desde 1857."
        },
        {
            "text": "Quantos fusos horários existem no Brasil?",
            "category": "geografia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["2", "3", "4", "5"],
            "correct_answer": "4",
            "explanation": "O Brasil possui 4 fusos horários diferentes."
        },
        
        # GEOGRAFIA - DIFÍCIL
        {
            "text": "Qual é o ponto mais profundo dos oceanos?",
            "category": "geografia",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["Fossa de Porto Rico", "Fossa das Marianas", "Fossa de Java", "Fossa das Filipinas"],
            "correct_answer": "Fossa das Marianas",
            "explanation": "A Fossa das Marianas tem cerca de 11.000 metros de profundidade."
        },
        {
            "text": "Qual país tem costa nos oceanos Atlântico e Pacífico?",
            "category": "geografia",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["México", "Colômbia", "Chile", "Canadá"],
            "correct_answer": "Colômbia",
            "explanation": "A Colômbia é banhada tanto pelo Oceano Atlântico quanto pelo Pacífico."
        },
        
        # ========== MAIS HISTÓRIA ==========
        
        # HISTÓRIA - FÁCIL
        {
            "text": "Quem foi o primeiro presidente do Brasil?",
            "category": "historia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Getúlio Vargas", "Deodoro da Fonseca", "Juscelino Kubitschek", "Dom Pedro II"],
            "correct_answer": "Deodoro da Fonseca",
            "explanation": "Marechal Deodoro da Fonseca foi o primeiro presidente do Brasil (1889-1891)."
        },
        {
            "text": "Em que ano terminou a Segunda Guerra Mundial?",
            "category": "historia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["1943", "1944", "1945", "1946"],
            "correct_answer": "1945",
            "explanation": "A Segunda Guerra Mundial terminou em 1945."
        },
        {
            "text": "Quem descobriu o Brasil?",
            "category": "historia",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernando de Magalhães"],
            "correct_answer": "Pedro Álvares Cabral",
            "explanation": "Pedro Álvares Cabral chegou ao Brasil em 22 de abril de 1500."
        },
        
        # HISTÓRIA - MÉDIO
        {
            "text": "Em que ano foi abolida a escravidão no Brasil?",
            "category": "historia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["1850", "1871", "1888", "1889"],
            "correct_answer": "1888",
            "explanation": "A Lei Áurea foi assinada pela Princesa Isabel em 13 de maio de 1888."
        },
        {
            "text": "Quem foi o imperador do Brasil por mais tempo?",
            "category": "historia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Dom Pedro I", "Dom Pedro II", "Dom João VI", "Dom Pedro de Alcântara"],
            "correct_answer": "Dom Pedro II",
            "explanation": "Dom Pedro II reinou por 58 anos (1831-1889)."
        },
        {
            "text": "Em que ano caiu o Muro de Berlim?",
            "category": "historia",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["1985", "1987", "1989", "1991"],
            "correct_answer": "1989",
            "explanation": "O Muro de Berlim caiu em 9 de novembro de 1989."
        },
        
        # HISTÓRIA - DIFÍCIL
        {
            "text": "Quem foi o líder da Revolução Cubana?",
            "category": "historia",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["Che Guevara", "Fidel Castro", "Hugo Chávez", "Salvador Allende"],
            "correct_answer": "Fidel Castro",
            "explanation": "Fidel Castro liderou a Revolução Cubana em 1959."
        },
        
        # ========== MAIS CIÊNCIAS ==========
        
        # CIÊNCIAS - FÁCIL
        {
            "text": "Qual é o gás mais abundante na atmosfera terrestre?",
            "category": "ciencias",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Oxigênio", "Nitrogênio", "Gás Carbônico", "Hidrogênio"],
            "correct_answer": "Nitrogênio",
            "explanation": "O nitrogênio representa cerca de 78% da atmosfera terrestre."
        },
        {
            "text": "Quantos planetas existem no Sistema Solar?",
            "category": "ciencias",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["7", "8", "9", "10"],
            "correct_answer": "8",
            "explanation": "Há 8 planetas no Sistema Solar (Plutão foi reclassificado como planeta anão)."
        },
        {
            "text": "Qual é a fórmula química da água?",
            "category": "ciencias",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["H2O", "CO2", "O2", "H2O2"],
            "correct_answer": "H2O",
            "explanation": "A água é composta por dois átomos de hidrogênio e um de oxigênio (H2O)."
        },
        
        # CIÊNCIAS - MÉDIO
        {
            "text": "Qual é o menor osso do corpo humano?",
            "category": "ciencias",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Estribo", "Martelo", "Bigorna", "Falange"],
            "correct_answer": "Estribo",
            "explanation": "O estribo, localizado no ouvido médio, tem apenas 2,5mm de comprimento."
        },
        {
            "text": "Quem desenvolveu a teoria da evolução?",
            "category": "ciencias",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Isaac Newton", "Charles Darwin", "Albert Einstein", "Galileu Galilei"],
            "correct_answer": "Charles Darwin",
            "explanation": "Charles Darwin publicou 'A Origem das Espécies' em 1859."
        },
        {
            "text": "Qual é o elemento químico mais abundante no universo?",
            "category": "ciencias",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Oxigênio", "Carbono", "Hidrogênio", "Hélio"],
            "correct_answer": "Hidrogênio",
            "explanation": "O hidrogênio representa cerca de 75% da massa do universo."
        },
        
        # CIÊNCIAS - DIFÍCIL
        {
            "text": "Quantos cromossomos tem uma célula humana normal?",
            "category": "ciencias",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["23", "42", "46", "48"],
            "correct_answer": "46",
            "explanation": "As células humanas normais possuem 46 cromossomos (23 pares)."
        },
        {
            "text": "Qual é a temperatura do zero absoluto?",
            "category": "ciencias",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["-273,15°C", "-100°C", "0°C", "-373,15°C"],
            "correct_answer": "-273,15°C",
            "explanation": "O zero absoluto é -273,15°C ou 0 Kelvin."
        },
        
        # ========== MAIS ESPORTES ==========
        
        # ESPORTES - FÁCIL
        {
            "text": "Qual país sediou a Copa do Mundo de 2014?",
            "category": "esportes",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Argentina", "Brasil", "Alemanha", "Rússia"],
            "correct_answer": "Brasil",
            "explanation": "O Brasil sediou a Copa do Mundo FIFA de 2014."
        },
        {
            "text": "Quantos jogadores formam uma equipe de vôlei?",
            "category": "esportes",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["5", "6", "7", "8"],
            "correct_answer": "6",
            "explanation": "Cada equipe de vôlei tem 6 jogadores em quadra."
        },
        {
            "text": "Em que esporte se usa uma raquete?",
            "category": "esportes",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Futebol", "Basquete", "Tênis", "Natação"],
            "correct_answer": "Tênis",
            "explanation": "O tênis é jogado com raquetes."
        },
        
        # ESPORTES - MÉDIO
        {
            "text": "Quantas vezes o Brasil foi campeão da Copa do Mundo?",
            "category": "esportes",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["3", "4", "5", "6"],
            "correct_answer": "5",
            "explanation": "O Brasil é pentacampeão mundial (1958, 1962, 1970, 1994, 2002)."
        },
        {
            "text": "Qual nadador brasileiro ganhou medalha de ouro nas Olimpíadas de 2016?",
            "category": "esportes",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["César Cielo", "Gustavo Borges", "Thiago Pereira", "Nenhum"],
            "correct_answer": "Nenhum",
            "explanation": "Nenhum nadador brasileiro ganhou ouro nas Olimpíadas do Rio 2016."
        },
        
        # ESPORTES - DIFÍCIL
        {
            "text": "Em que ano Ayrton Senna morreu?",
            "category": "esportes",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["1992", "1993", "1994", "1995"],
            "correct_answer": "1994",
            "explanation": "Ayrton Senna faleceu em 1º de maio de 1994 no GP de San Marino."
        },
        
        # ========== MAIS GERAL ==========
        
        # GERAL - FÁCIL
        {
            "text": "Quantas horas tem um dia?",
            "category": "geral",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["12", "24", "36", "48"],
            "correct_answer": "24",
            "explanation": "Um dia tem 24 horas."
        },
        {
            "text": "Qual é a cor da bandeira do Brasil?",
            "category": "geral",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["Verde, amarelo, azul e branco", "Verde e amarelo", "Azul e branco", "Verde, vermelho e branco"],
            "correct_answer": "Verde, amarelo, azul e branco",
            "explanation": "A bandeira do Brasil tem verde, amarelo, azul e branco."
        },
        {
            "text": "Quantos minutos tem uma hora?",
            "category": "geral",
            "difficulty": "facil",
            "question_type": "multiple_choice",
            "options": ["30", "60", "90", "120"],
            "correct_answer": "60",
            "explanation": "Uma hora tem 60 minutos."
        },
        
        # GERAL - MÉDIO
        {
            "text": "Qual é o maior mamífero terrestre?",
            "category": "geral",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Rinoceronte", "Hipopótamo", "Elefante africano", "Girafa"],
            "correct_answer": "Elefante africano",
            "explanation": "O elefante africano pode pesar até 6 toneladas."
        },
        {
            "text": "Quantos estados tem o Brasil?",
            "category": "geral",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["24", "25", "26", "27"],
            "correct_answer": "26",
            "explanation": "O Brasil tem 26 estados mais o Distrito Federal."
        },
        {
            "text": "Qual é o animal terrestre mais rápido do mundo?",
            "category": "geral",
            "difficulty": "medio",
            "question_type": "multiple_choice",
            "options": ["Leão", "Guepardo", "Antílope", "Cavalo"],
            "correct_answer": "Guepardo",
            "explanation": "O guepardo pode atingir até 120 km/h."
        },
        
        # GERAL - DIFÍCIL
        {
            "text": "Qual é a moeda do Japão?",
            "category": "geral",
            "difficulty": "dificil",
            "question_type": "multiple_choice",
            "options": ["Yuan", "Won", "Yen", "Rupia"],
            "correct_answer": "Yen",
            "explanation": "A moeda oficial do Japão é o Yen (¥)."
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