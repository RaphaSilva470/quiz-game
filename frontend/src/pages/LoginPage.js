import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LoginPage.css';

function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
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

    if (!formData.email || !formData.password) {
      setError('Por favor, preencha todos os campos');
      return;
    }

    try {
      // --- MUDANÇA AQUI: Verificar no LocalStorage ---
      
      // 1. Busca o usuário salvo no registro
      const storedUser = localStorage.getItem('testUser');
      
      if (!storedUser) {
        setError('Nenhum usuário registrado para teste. Crie uma conta primeiro.');
        return;
      }

      const validUser = JSON.parse(storedUser);

      // 2. Verifica se email e senha batem
      if (formData.email === validUser.email && formData.password === validUser.password) {
        console.log('Login realizado com sucesso!');
        // Redirecione para onde quiser (ex: dashboard ou home)
        navigate('/dashboard'); 
      } else {
        setError('Email ou senha incorretos.');
      }
      // ------------------------------------------------

    } catch (err) {
      setError('Erro ao fazer login.');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <h1>Bem-vindo de volta!</h1>
            <p>Faça login para continuar</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            {error && <div className="error-message">{error}</div>}

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
                placeholder="••••••••"
                required
              />
            </div>

            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" />
                <span>Lembrar-me</span>
              </label>
              <Link to="/forgot-password" className="forgot-link">
                Esqueceu a senha?
              </Link>
            </div>

            <button type="submit" className="submit-button">
              Entrar
            </button>
          </form>

          <div className="login-footer">
            <p>
              Não tem uma conta?{' '}
              <Link to="/register" className="link">
                Criar conta
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

export default LoginPage;

