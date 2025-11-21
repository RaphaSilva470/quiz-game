import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css';

function LandingPage() {
  return (
    <div className="landing-page">
      <div className="landing-container">
        <div className="landing-content">
          <h1 className="landing-title">Quiz Game</h1>
          <p className="landing-subtitle">
            Teste seus conhecimentos e desafie-se com nossos quizzes!
          </p>
          <p className="landing-description">
            Participe de quizzes interativos, acompanhe seu progresso e 
            compare seus resultados com outros jogadores.
          </p>
          <div className="landing-buttons">
            <Link to="/login" className="btn btn-primary">
              Entrar
            </Link>
            <Link to="/register" className="btn btn-secondary">
              Criar Conta
            </Link>
          </div>
        </div>
        <div className="landing-features">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Desafios Variados</h3>
            <p>Diversos temas e níveis de dificuldade</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Acompanhe Progresso</h3>
            <p>Veja suas estatísticas e melhorias</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🏆</div>
            <h3>Ranking</h3>
            <p>Compare seus resultados com outros</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;

