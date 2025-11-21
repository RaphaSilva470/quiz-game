import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from './LoginPage';
import '@testing-library/jest-dom';

// 1. Mock do React Router
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  Link: ({ children, to }) => <a href={to}>{children}</a>,
  useNavigate: () => mockNavigate,
}));

// 2. Mock do LocalStorage COMPLETO
const localStorageMock = (function () {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('LoginPage', () => {
  beforeEach(() => {
    localStorageMock.clear();
    mockNavigate.mockClear();
    // Limpa mocks para evitar sujeira entre testes
    localStorageMock.getItem.mockClear();
  });

  test('renders login form', () => {
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });

  test('shows error when user does not exist in localStorage', async () => {
    // NÃO criamos usuário aqui propositalmente
    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'ghost@test.com' } });
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: '123456' } });
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    expect(await screen.findByText(/nenhum usuário registrado/i)).toBeInTheDocument();
  });

  test('shows error with incorrect credentials', async () => {
    // 1. CRIA O USUÁRIO FALSO ANTES (SEED)
    const fakeUser = JSON.stringify({
      email: 'test@test.com',
      password: 'password123'
    });
    localStorageMock.getItem.mockReturnValue(fakeUser);

    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    // 2. Tenta logar com senha ERRADA
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@test.com' } });
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: 'WRONG_PASS' } });
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    // Agora ele passa dessa fase porque o usuário existe, e barra na senha
    expect(await screen.findByText(/email ou senha incorretos/i)).toBeInTheDocument();
  });

  test('navigates to dashboard on successful login', async () => {
    // 1. CRIA O USUÁRIO FALSO ANTES (SEED)
    const fakeUser = JSON.stringify({
      email: 'test@test.com',
      password: 'password123'
    });
    localStorageMock.getItem.mockReturnValue(fakeUser);

    render(
      <BrowserRouter>
        <LoginPage />
      </BrowserRouter>
    );

    // 2. Loga com dados CERTOS
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@test.com' } });
    fireEvent.change(screen.getByLabelText(/senha/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));

    await waitFor(() => {
        expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });
});