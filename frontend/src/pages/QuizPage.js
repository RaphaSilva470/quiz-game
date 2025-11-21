import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './QuizPage.css';

function QuizPage() {
  const [quizData, setQuizData] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState('');
  const [timeStarted, setTimeStarted] = useState(null);
  const [timeElapsed, setTimeElapsed] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [answerResult, setAnswerResult] = useState(null);
  const [score, setScore] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    // TODO: Buscar dados do quiz da API
    // Por enquanto, usando dados mockados
    const savedQuiz = sessionStorage.getItem('currentQuiz');
    if (savedQuiz) {
      const quiz = JSON.parse(savedQuiz);
      // Mock de perguntas
      const mockQuestions = [
        {
          id: 1,
          text: 'Qual é a capital do Brasil?',
          options: ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Belo Horizonte'],
          correct_answer: 'Brasília'
        },
        {
          id: 2,
          text: 'Em que ano o Brasil foi descoberto?',
          options: ['1498', '1500', '1502', '1499'],
          correct_answer: '1500'
        },
        {
          id: 3,
          text: 'Qual é o maior planeta do sistema solar?',
          options: ['Terra', 'Júpiter', 'Saturno', 'Netuno'],
          correct_answer: 'Júpiter'
        }
      ];
      setQuizData({
        ...quiz,
        questions: mockQuestions.slice(0, quiz.num_questions || 10)
      });
    } else {
      navigate('/quiz-setup');
    }
  }, [navigate]);

  useEffect(() => {
    if (quizData && currentQuestionIndex < quizData.questions.length) {
      setTimeStarted(Date.now());
      setSelectedAnswer('');
      setShowResult(false);
      setAnswerResult(null);
    }
  }, [currentQuestionIndex, quizData]);

  useEffect(() => {
    if (timeStarted && !showResult) {
      const interval = setInterval(() => {
        setTimeElapsed(Math.floor((Date.now() - timeStarted) / 1000));
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [timeStarted, showResult]);

  const handleAnswerSelect = (answer) => {
    if (!showResult) {
      setSelectedAnswer(answer);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!selectedAnswer) return;

    const currentQuestion = quizData.questions[currentQuestionIndex];
    const isCorrect = selectedAnswer === currentQuestion.correct_answer;
    const timeTaken = timeElapsed;

    // TODO: Enviar resposta para API
    // Por enquanto, apenas atualizar estado local
    setAnswerResult({
      is_correct: isCorrect,
      correct_answer: currentQuestion.correct_answer,
      points_earned: isCorrect ? 10 : 0
    });

    if (isCorrect) {
      setScore(score + 10);
    }

    setShowResult(true);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < quizData.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // Finalizar quiz
      handleFinishQuiz();
    }
  };

  const handleFinishQuiz = async () => {
    // TODO: Chamar API para finalizar quiz
    const results = {
      quiz_id: quizData.quiz_id,
      final_score: score,
      total_questions: quizData.questions.length,
      correct_answers: Math.floor(score / 10),
      accuracy: (Math.floor(score / 10) / quizData.questions.length) * 100
    };
    
    sessionStorage.setItem('quizResults', JSON.stringify(results));
    navigate('/results');
  };

  if (!quizData) {
    return <div className="quiz-page loading">Carregando...</div>;
  }

  const currentQuestion = quizData.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / quizData.questions.length) * 100;
  const isLastQuestion = currentQuestionIndex === quizData.questions.length - 1;

  return (
    <div className="quiz-page">
      <div className="quiz-container">
        <div className="quiz-header">
          <div className="quiz-progress">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="progress-text">
              Pergunta {currentQuestionIndex + 1} de {quizData.questions.length}
            </div>
          </div>
          <div className="quiz-score">
            Pontuação: {score}
          </div>
        </div>

        <div className="question-card">
          <div className="question-header">
            <div className="question-timer">
              ⏱️ {timeElapsed}s
            </div>
          </div>

          <h2 className="question-text">{currentQuestion.text}</h2>

          <div className="answers-grid">
            {currentQuestion.options.map((option, index) => (
              <button
                key={index}
                className={`answer-option ${
                  showResult
                    ? option === currentQuestion.correct_answer
                      ? 'correct'
                      : selectedAnswer === option && !answerResult.is_correct
                      ? 'incorrect'
                      : ''
                    : selectedAnswer === option
                    ? 'selected'
                    : ''
                }`}
                onClick={() => handleAnswerSelect(option)}
                disabled={showResult}
              >
                {option}
              </button>
            ))}
          </div>

          {showResult && (
            <div className={`result-feedback ${answerResult.is_correct ? 'correct' : 'incorrect'}`}>
              <div className="result-icon">
                {answerResult.is_correct ? '✓' : '✗'}
              </div>
              <div className="result-text">
                {answerResult.is_correct 
                  ? `Correto! +${answerResult.points_earned} pontos`
                  : `Incorreto. A resposta correta é: ${answerResult.correct_answer}`
                }
              </div>
            </div>
          )}

          <div className="quiz-actions">
            {!showResult ? (
              <button
                onClick={handleSubmitAnswer}
                disabled={!selectedAnswer}
                className="btn btn-primary"
              >
                Confirmar Resposta
              </button>
            ) : (
              <button
                onClick={handleNextQuestion}
                className="btn btn-primary"
              >
                {isLastQuestion ? 'Ver Resultados' : 'Próxima Pergunta'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default QuizPage;

