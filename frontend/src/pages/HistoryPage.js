import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './HistoryPage.css';

function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState({ category: '', difficulty: '' });

  useEffect(() => {
    // TODO: Buscar histórico da API /api/quiz/history
    // Por enquanto, usando dados mockados
    const mockHistory = [
      {
        quiz_id: 1,
        category: 'geografia',
        difficulty: 'medio',
        final_score: 85,
        correct_answers: 8,
        total_questions: 10,
        accuracy: 80.0,
        completed_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        quiz_id: 2,
        category: 'historia',
        difficulty: 'facil',
        final_score: 100,
        correct_answers: 10,
        total_questions: 10,
        accuracy: 100.0,
        completed_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        quiz_id: 3,
        category: 'ciencias',
        difficulty: 'dificil',
        final_score: 60,
        correct_answers: 6,
        total_questions: 10,
        accuracy: 60.0,
        completed_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        quiz_id: 4,
        category: 'esportes',
        difficulty: 'medio',
        final_score: 90,
        correct_answers: 9,
        total_questions: 10,
        accuracy: 90.0,
        completed_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        quiz_id: 5,
        category: 'geral',
        difficulty: 'medio',
        final_score: 75,
        correct_answers: 7,
        total_questions: 10,
        accuracy: 70.0,
        completed_at: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString()
      },
      {
        quiz_id: 6,
        category: 'geografia',
        difficulty: 'facil',
        final_score: 95,
        correct_answers: 9,
        total_questions: 10,
        accuracy: 90.0,
        completed_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString()
      }
    ];
    
    setHistory(mockHistory);
    setLoading(false);
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Hoje';
    } else if (diffDays === 1) {
      return 'Ontem';
    } else if (diffDays < 7) {
      return `${diffDays} dias atrás`;
    } else {
      return date.toLocaleDateString('pt-BR');
    }
  };

  const getAccuracyColor = (accuracy) => {
    if (accuracy >= 80) return 'excellent';
    if (accuracy >= 60) return 'good';
    return 'poor';
  };

  const filteredHistory = history.filter(quiz => {
    if (filter.category && quiz.category !== filter.category) return false;
    if (filter.difficulty && quiz.difficulty !== filter.difficulty) return false;
    return true;
  });

  const categories = [
    { value: '', label: 'Todas' },
    { value: 'geografia', label: 'Geografia' },
    { value: 'historia', label: 'História' },
    { value: 'ciencias', label: 'Ciências' },
    { value: 'esportes', label: 'Esportes' },
    { value: 'geral', label: 'Geral' }
  ];

  const difficulties = [
    { value: '', label: 'Todas' },
    { value: 'facil', label: 'Fácil' },
    { value: 'medio', label: 'Médio' },
    { value: 'dificil', label: 'Difícil' }
  ];

  if (loading) {
    return (
      <div className="history-page">
        <div className="history-container">
          <div className="loading">Carregando histórico...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="history-page">
      <div className="history-container">
        <div className="history-header">
          <h1>📜 Histórico</h1>
          <p>Seus quizzes completados</p>
        </div>

        <div className="history-filters">
          <div className="filter-group">
            <label htmlFor="category-filter">Categoria:</label>
            <select
              id="category-filter"
              value={filter.category}
              onChange={(e) => setFilter({ ...filter, category: e.target.value })}
              className="filter-select"
            >
              {categories.map((cat) => (
                <option key={cat.value} value={cat.value}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label htmlFor="difficulty-filter">Dificuldade:</label>
            <select
              id="difficulty-filter"
              value={filter.difficulty}
              onChange={(e) => setFilter({ ...filter, difficulty: e.target.value })}
              className="filter-select"
            >
              {difficulties.map((diff) => (
                <option key={diff.value} value={diff.value}>
                  {diff.label}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-reset">
            <button
              onClick={() => setFilter({ category: '', difficulty: '' })}
              className="btn-reset"
            >
              Limpar Filtros
            </button>
          </div>
        </div>

        {filteredHistory.length > 0 ? (
          <div className="history-list">
            {filteredHistory.map((quiz) => (
              <div key={quiz.quiz_id} className="history-item">
                <div className="history-main">
                  <div className="history-info">
                    <div className="history-category">
                      <span className="category-badge">
                        {quiz.category ? quiz.category.charAt(0).toUpperCase() + quiz.category.slice(1) : 'Geral'}
                      </span>
                      <span className="difficulty-badge">
                        {quiz.difficulty ? quiz.difficulty.charAt(0).toUpperCase() + quiz.difficulty.slice(1) : 'Médio'}
                      </span>
                    </div>
                    <div className="history-date">
                      {formatDate(quiz.completed_at)}
                    </div>
                  </div>

                  <div className="history-stats">
                    <div className="history-score">
                      <span className="score-label">Pontuação:</span>
                      <span className="score-value">{quiz.final_score}</span>
                    </div>
                    <div className="history-accuracy">
                      <span className={`accuracy-badge ${getAccuracyColor(quiz.accuracy)}`}>
                        {quiz.accuracy.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>

                <div className="history-details">
                  <div className="detail-item">
                    <span className="detail-label">Corretas:</span>
                    <span className="detail-value correct">{quiz.correct_answers}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Total:</span>
                    <span className="detail-value">{quiz.total_questions}</span>
                  </div>
                  <div className="detail-item">
                    <span className="detail-label">Taxa de Acerto:</span>
                    <span className="detail-value">{quiz.accuracy.toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="empty-history">
            <p>Nenhum quiz encontrado com os filtros selecionados.</p>
            <Link to="/quiz-setup" className="btn btn-primary">
              Fazer Novo Quiz
            </Link>
          </div>
        )}

        <div className="history-actions">
          <Link to="/dashboard" className="btn btn-primary">
            Voltar ao Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

export default HistoryPage;

