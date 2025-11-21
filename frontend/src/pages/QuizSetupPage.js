import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './QuizSetupPage.css';

function QuizSetupPage() {
  const [formData, setFormData] = useState({
    category: '',
    difficulty: '',
    num_questions: 10
  });
  const navigate = useNavigate();

  const categories = [
    { value: '', label: 'Todas' },
    { value: 'geografia', label: 'Geografia' },
    { value: 'historia', label: 'História' },
    { value: 'ciencias', label: 'Ciências' },
    { value: 'esportes', label: 'Esportes' },
    { value: 'geral', label: 'Geral' }
  ];

  const difficulties = [
    { value: '', label: 'Qualquer' },
    { value: 'facil', label: 'Fácil' },
    { value: 'medio', label: 'Médio' },
    { value: 'dificil', label: 'Difícil' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'num_questions' ? parseInt(value) : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // TODO: Chamar API para iniciar quiz
    // Por enquanto, navegando para a tela de quiz com dados mockados
    const quizData = {
      quiz_id: Math.floor(Math.random() * 1000),
      ...formData
    };
    
    // Salvar dados temporariamente (em produção, viria da API)
    sessionStorage.setItem('currentQuiz', JSON.stringify(quizData));
    
    navigate('/quiz');
  };

  return (
    <div className="quiz-setup-page">
      <div className="setup-container">
        <div className="setup-card">
          <div className="setup-header">
            <h1>Configurar Quiz</h1>
            <p>Escolha as opções para seu quiz</p>
          </div>

          <form onSubmit={handleSubmit} className="setup-form">
            <div className="form-group">
              <label htmlFor="category">Categoria</label>
              <select
                id="category"
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="form-select"
              >
                {categories.map((cat) => (
                  <option key={cat.value} value={cat.value}>
                    {cat.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="difficulty">Dificuldade</label>
              <select
                id="difficulty"
                name="difficulty"
                value={formData.difficulty}
                onChange={handleChange}
                className="form-select"
              >
                {difficulties.map((diff) => (
                  <option key={diff.value} value={diff.value}>
                    {diff.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="num_questions">
                Número de Perguntas: {formData.num_questions}
              </label>
              <input
                type="range"
                id="num_questions"
                name="num_questions"
                min="5"
                max="20"
                value={formData.num_questions}
                onChange={handleChange}
                className="form-range"
              />
              <div className="range-labels">
                <span>5</span>
                <span>20</span>
              </div>
            </div>

            <div className="form-actions">
              <button type="button" onClick={() => navigate('/dashboard')} className="btn btn-secondary">
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary">
                Iniciar Quiz
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default QuizSetupPage;

