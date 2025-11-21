import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './StatsPage.css';

function StatsPage() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Buscar estatísticas da API /api/users/me/stats
    // Por enquanto, usando dados mockados
    const mockStats = {
      user_id: 1,
      username: 'teste',
      overall: {
        total_quizzes: 15,
        total_questions: 150,
        correct_answers: 120,
        incorrect_answers: 30,
        accuracy: 80.0,
        total_score: 1200,
        average_score: 80.0,
        best_score: 100,
        worst_score: 50,
        total_time_played: 3600
      },
      by_difficulty: {
        facil: {
          quizzes: 5,
          questions: 50,
          correct: 45,
          accuracy: 90.0,
          average_score: 90.0
        },
        medio: {
          quizzes: 8,
          questions: 80,
          correct: 64,
          accuracy: 80.0,
          average_score: 80.0
        },
        dificil: {
          quizzes: 2,
          questions: 20,
          correct: 11,
          accuracy: 55.0,
          average_score: 55.0
        }
      },
      by_category: {
        geografia: {
          quizzes: 4,
          questions: 40,
          correct: 32,
          accuracy: 80.0
        },
        historia: {
          quizzes: 3,
          questions: 30,
          correct: 24,
          accuracy: 80.0
        },
        ciencias: {
          quizzes: 5,
          questions: 50,
          correct: 40,
          accuracy: 80.0
        },
        esportes: {
          quizzes: 2,
          questions: 20,
          correct: 16,
          accuracy: 80.0
        },
        geral: {
          quizzes: 1,
          questions: 10,
          correct: 8,
          accuracy: 80.0
        }
      }
    };
    
    setStats(mockStats);
    setLoading(false);
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}min`;
    }
    return `${minutes}min`;
  };

  if (loading) {
    return (
      <div className="stats-page">
        <div className="stats-container">
          <div className="loading">Carregando estatísticas...</div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="stats-page">
        <div className="stats-container">
          <div className="no-stats">
            <p>Nenhuma estatística disponível ainda.</p>
            <Link to="/quiz-setup" className="btn btn-primary">
              Fazer Primeiro Quiz
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="stats-page">
      <div className="stats-container">
        <div className="stats-header">
          <h1>📊 Estatísticas</h1>
          <p>Desempenho de {stats.username}</p>
        </div>

        <div className="stats-section">
          <h2>Visão Geral</h2>
          <div className="overall-stats">
            <div className="stat-card large">
              <div className="stat-icon">🎯</div>
              <div className="stat-value">{stats.overall.total_quizzes}</div>
              <div className="stat-label">Quizzes Completos</div>
            </div>
            <div className="stat-card large">
              <div className="stat-icon">⭐</div>
              <div className="stat-value">{stats.overall.total_score}</div>
              <div className="stat-label">Pontuação Total</div>
            </div>
            <div className="stat-card large">
              <div className="stat-icon">✅</div>
              <div className="stat-value">{stats.overall.accuracy.toFixed(1)}%</div>
              <div className="stat-label">Precisão</div>
            </div>
            <div className="stat-card large">
              <div className="stat-icon">⏱️</div>
              <div className="stat-value">{formatTime(stats.overall.total_time_played)}</div>
              <div className="stat-label">Tempo Total</div>
            </div>
          </div>

          <div className="detailed-stats">
            <div className="detail-item">
              <span className="detail-label">Total de Perguntas:</span>
              <span className="detail-value">{stats.overall.total_questions}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Respostas Corretas:</span>
              <span className="detail-value correct">{stats.overall.correct_answers}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Respostas Incorretas:</span>
              <span className="detail-value incorrect">{stats.overall.incorrect_answers}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Pontuação Média:</span>
              <span className="detail-value">{stats.overall.average_score.toFixed(1)}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Melhor Pontuação:</span>
              <span className="detail-value best">{stats.overall.best_score}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Pior Pontuação:</span>
              <span className="detail-value worst">{stats.overall.worst_score}</span>
            </div>
          </div>
        </div>

        <div className="stats-section">
          <h2>Por Dificuldade</h2>
          <div className="difficulty-stats">
            {Object.entries(stats.by_difficulty).map(([difficulty, data]) => (
              <div key={difficulty} className="difficulty-card">
                <div className="difficulty-header">
                  <h3>{difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}</h3>
                  <div className="difficulty-badge">{data.quizzes} quizzes</div>
                </div>
                <div className="difficulty-content">
                  <div className="difficulty-stat">
                    <span>Precisão:</span>
                    <strong>{data.accuracy.toFixed(1)}%</strong>
                  </div>
                  <div className="difficulty-stat">
                    <span>Pontuação Média:</span>
                    <strong>{data.average_score.toFixed(1)}</strong>
                  </div>
                  <div className="difficulty-stat">
                    <span>Corretas:</span>
                    <strong>{data.correct}/{data.questions}</strong>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="stats-section">
          <h2>Por Categoria</h2>
          <div className="category-stats">
            {Object.entries(stats.by_category).map(([category, data]) => (
              <div key={category} className="category-card">
                <div className="category-name">
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </div>
                <div className="category-info">
                  <div className="category-stat">
                    <span className="category-label">Quizzes:</span>
                    <span className="category-value">{data.quizzes}</span>
                  </div>
                  <div className="category-stat">
                    <span className="category-label">Precisão:</span>
                    <span className="category-value">{data.accuracy.toFixed(1)}%</span>
                  </div>
                  <div className="category-stat">
                    <span className="category-label">Corretas:</span>
                    <span className="category-value">{data.correct}/{data.questions}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="stats-actions">
          <Link to="/dashboard" className="btn btn-primary">
            Voltar ao Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

export default StatsPage;

