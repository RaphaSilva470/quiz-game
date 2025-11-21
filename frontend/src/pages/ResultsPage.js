import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import './ResultsPage.css';

function ResultsPage() {
  const [results, setResults] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // TODO: Buscar resultados da API
    const savedResults = sessionStorage.getItem('quizResults');
    if (savedResults) {
      setResults(JSON.parse(savedResults));
    } else {
      navigate('/dashboard');
    }
  }, [navigate]);

  if (!results) {
    return <div className="results-page loading">Carregando...</div>;
  }

  const accuracy = results.accuracy || 0;
  const isExcellent = accuracy >= 80;
  const isGood = accuracy >= 60;
  const performanceEmoji = isExcellent ? '🎉' : isGood ? '👍' : '💪';
  const performanceText = isExcellent 
    ? 'Excelente!' 
    : isGood 
    ? 'Bom trabalho!' 
    : 'Continue praticando!';

  return (
    <div className="results-page">
      <div className="results-container">
        <div className="results-card">
          <div className="results-header">
            <div className="results-emoji">{performanceEmoji}</div>
            <h1>{performanceText}</h1>
            <p>Quiz Finalizado</p>
          </div>

          <div className="results-stats">
            <div className="stat-large">
              <div className="stat-value">{results.final_score}</div>
              <div className="stat-label">Pontuação Total</div>
            </div>

            <div className="stats-grid">
              <div className="stat-item">
                <div className="stat-number">{results.correct_answers}</div>
                <div className="stat-text">Corretas</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">
                  {results.total_questions - results.correct_answers}
                </div>
                <div className="stat-text">Incorretas</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">{results.total_questions}</div>
                <div className="stat-text">Total</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">{accuracy.toFixed(1)}%</div>
                <div className="stat-text">Precisão</div>
              </div>
            </div>

            <div className="accuracy-bar">
              <div className="accuracy-label">Precisão</div>
              <div className="accuracy-fill-container">
                <div 
                  className="accuracy-fill"
                  style={{ width: `${accuracy}%` }}
                ></div>
              </div>
              <div className="accuracy-percentage">{accuracy.toFixed(1)}%</div>
            </div>
          </div>

          <div className="results-actions">
            <Link to="/quiz-setup" className="btn btn-primary">
              Fazer Outro Quiz
            </Link>
            <Link to="/ranking" className="btn btn-secondary">
              Ver Ranking
            </Link>
            <Link to="/dashboard" className="btn btn-outline">
              Voltar ao Dashboard
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsPage;

