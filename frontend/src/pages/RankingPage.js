import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './RankingPage.css';

function RankingPage() {
  const [ranking, setRanking] = useState([]);
  const [userPosition, setUserPosition] = useState(null);
  const [totalUsers, setTotalUsers] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // TODO: Buscar ranking da API
    // Por enquanto, usando dados mockados
    const mockRanking = [
      { position: 1, username: 'Jogador1', total_score: 2500, total_quizzes: 25, accuracy: 92.5 },
      { position: 2, username: 'Jogador2', total_score: 2300, total_quizzes: 22, accuracy: 89.3 },
      { position: 3, username: 'Jogador3', total_score: 2100, total_quizzes: 20, accuracy: 87.1 },
      { position: 4, username: 'Jogador4', total_score: 1950, total_quizzes: 18, accuracy: 85.0 },
      { position: 5, username: 'Jogador5', total_score: 1800, total_quizzes: 17, accuracy: 82.4 },
      { position: 6, username: 'Jogador6', total_score: 1650, total_quizzes: 15, accuracy: 80.0 },
      { position: 7, username: 'Jogador7', total_score: 1500, total_quizzes: 14, accuracy: 78.5 },
      { position: 8, username: 'Jogador8', total_score: 1350, total_quizzes: 13, accuracy: 76.2 },
      { position: 9, username: 'Jogador9', total_score: 1200, total_quizzes: 12, accuracy: 74.0 },
      { position: 10, username: 'Jogador10', total_score: 1100, total_quizzes: 11, accuracy: 72.5 }
    ];
    
    setRanking(mockRanking);
    setUserPosition(15);
    setTotalUsers(150);
    setLoading(false);
  }, []);

  const getMedalEmoji = (position) => {
    if (position === 1) return '🥇';
    if (position === 2) return '🥈';
    if (position === 3) return '🥉';
    return position;
  };

  if (loading) {
    return (
      <div className="ranking-page">
        <div className="ranking-container">
          <div className="loading">Carregando ranking...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="ranking-page">
      <div className="ranking-container">
        <div className="ranking-header">
          <h1>🏆 Ranking Global</h1>
          <p>Top {ranking.length} jogadores</p>
          {userPosition && (
            <div className="user-position">
              Sua posição: <strong>#{userPosition}</strong> de {totalUsers} jogadores
            </div>
          )}
        </div>

        <div className="ranking-list">
          {ranking.map((user, index) => (
            <div
              key={user.position}
              className={`ranking-item ${index < 3 ? 'top-three' : ''} ${index === 0 ? 'first' : ''}`}
            >
              <div className="rank-position">
                {getMedalEmoji(user.position)}
              </div>
              <div className="rank-info">
                <div className="rank-username">{user.username}</div>
                <div className="rank-stats">
                  <span>{user.total_quizzes} quizzes</span>
                  <span>•</span>
                  <span>{user.accuracy.toFixed(1)}% precisão</span>
                </div>
              </div>
              <div className="rank-score">
                {user.total_score.toLocaleString()} pts
              </div>
            </div>
          ))}
        </div>

        <div className="ranking-actions">
          <Link to="/dashboard" className="btn btn-primary">
            Voltar ao Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

export default RankingPage;

