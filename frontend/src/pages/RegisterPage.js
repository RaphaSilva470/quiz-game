import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './RegisterPage.css';

function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validação básica
    if (!formData.name || !formData.email || !formData.password || !formData.confirmPassword) {
      setError('Por favor, preencha todos os campos');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem');
      return;
    }

    if (formData.password.length < 6) {
      setError('A senha deve ter pelo menos 6 caracteres');
      return;
    }

    // TODO: Implementar chamada à API de registro
    try {
      // Simulação de registro - remover quando implementar API
      console.log('Register attempt:', {
        name: formData.name,
        email: formData.email,
        password: formData.password
      });
      // navigate('/login'); // Redirecionar após registro bem-sucedido
      alert('Registro funcionalidade será implementada com a API');
    } catch (err) {
      setError('Erro ao criar conta. Tente novamente.');
    }
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-card">
          <div className="register-header">
            <h1>Criar Conta</h1>
            <p>Preencha os dados para começar</p>
          </div>

          <form onSubmit={handleSubmit} className="register-form">
            {error && <div className="error-message">{error}</div>}

            <div className="form-group">
              <label htmlFor="name">Nome</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Seu nome completo"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="seu@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Senha</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Mínimo 6 caracteres"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmar Senha</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Digite a senha novamente"
                required
              />
            </div>

            <button type="submit" className="submit-button">
              Criar Conta
            </button>
          </form>

          <div className="register-footer">
            <p>
              Já tem uma conta?{' '}
              <Link to="/login" className="link">
                Fazer login
              </Link>
            </p>
          </div>

          <div className="back-link">
            <Link to="/" className="link">
              ← Voltar para a página inicial
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;

