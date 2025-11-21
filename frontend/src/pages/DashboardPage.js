import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './DashboardPage.css';

function DashboardPage() {
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    // TODO: Buscar dados do usuário, estatísticas e histórico da API
    // Por enquanto, usando dados mockados
    setUser({ username: 'Usuário', email: 'usuario@email.com' });
    setStats({
      total_quizzes: 15,
      total_score: 1250,
      correct_answers: 120,
      total_questions: 150,
      accuracy: 80.0
    });
    setHistory([
      {
        quiz_id: 1,
        category: 'geografia',
        difficulty: 'medio',
        final_score: 85,
        correct_answers: 8,
        total_questions: 10,
        accuracy: 80.0,
        completed_at: new Date().toISOString()
      }
    ]);
  }, []);

  const handleLogout = () => {
    // TODO: Implementar logout
    navigate('/');
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Dashboard</h1>
          <div className="user-info">
            <span>Olá, {user?.username || 'Usuário'}!</span>
            <button onClick={handleLogout} className="logout-btn">
              Sair
            </button>
          </div>
        </div>
      </div>

      <div className="dashboard-container">
        <div className="dashboard-main">
          <div className="quick-actions">
            <Link to="/quiz-setup" className="action-card primary">
              <div className="action-icon">🚀</div>
              <h2>Iniciar Quiz</h2>
              <p>Comece um novo desafio agora</p>
            </Link>
            <Link to="/stats" className="action-card">
              <div className="action-icon">📊</div>
              <h2>Estatísticas</h2>
              <p>Veja seu desempenho detalhado</p>
            </Link>
            <Link to="/history" className="action-card">
              <div className="action-icon">📜</div>
              <h2>Histórico</h2>
              <p>Revise seus quizzes anteriores</p>
            </Link>
            <Link to="/ranking" className="action-card">
              <div className="action-icon">🏆</div>
              <h2>Ranking</h2>
              <p>Veja sua posição global</p>
            </Link>
          </div>

          {stats && (
            <div className="stats-section">
              <h2>Estatísticas</h2>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-value">{stats.total_quizzes}</div>
                  <div className="stat-label">Quizzes Completos</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.total_score}</div>
                  <div className="stat-label">Pontuação Total</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.correct_answers}/{stats.total_questions}</div>
                  <div className="stat-label">Respostas Corretas</div>
                </div>
                <div className="stat-card">
                  <div className="stat-value">{stats.accuracy.toFixed(1)}%</div>
                  <div className="stat-label">Precisão</div>
                </div>
              </div>
            </div>
          )}

          <div className="history-section">
            <h2>Histórico Recente</h2>
            {history.length > 0 ? (
              <div className="history-list">
                {history.slice(0, 5).map((quiz) => (
                  <div key={quiz.quiz_id} className="history-item">
                    <div className="history-info">
                      <div className="history-category">
                        {quiz.category || 'Geral'} • {quiz.difficulty || 'Médio'}
                      </div>
                      <div className="history-score">
                        {quiz.correct_answers}/{quiz.total_questions} • {quiz.accuracy.toFixed(1)}%
                      </div>
                    </div>
                    <div className="history-points">
                      {quiz.final_score} pts
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-history">
                <p>Nenhum quiz completado ainda. Comece agora!</p>
                <Link to="/quiz-setup" className="btn btn-primary">
                  Iniciar Primeiro Quiz
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;

