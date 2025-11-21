import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import RegisterPage from './RegisterPage';

// 1. Mock do React Router Dom
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  Link: ({ children, to }) => <a href={to}>{children}</a>,
  useNavigate: () => mockNavigate,
}));

// 2. Mock do LocalStorage
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

// 3. Mock do window.alert (para não travar o teste)
window.alert = jest.fn();

describe('RegisterPage', () => {
  beforeEach(() => {
    localStorageMock.clear();
    mockNavigate.mockClear();
    window.alert.mockClear();
  });

  test('renders all input fields and button', () => {
    render(<RegisterPage />);

    expect(screen.getByLabelText(/nome/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    
    // CORREÇÃO: Usando ^ e $ para pegar EXATAMENTE "Senha"
    expect(screen.getByLabelText(/^senha$/i)).toBeInTheDocument();
    
    expect(screen.getByLabelText(/confirmar senha/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /criar conta/i })).toBeInTheDocument();
  });

  test('shows error when passwords do not match', () => {
    render(<RegisterPage />);

    fireEvent.change(screen.getByLabelText(/nome/i), { target: { value: 'Test User' } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@test.com' } });
    
    // CORREÇÃO NOS SELETORES
    fireEvent.change(screen.getByLabelText(/^senha$/i), { target: { value: '123456' } });
    fireEvent.change(screen.getByLabelText(/confirmar senha/i), { target: { value: '654321' } });

    fireEvent.click(screen.getByRole('button', { name: /criar conta/i }));

    expect(screen.getByText(/as senhas não coincidem/i)).toBeInTheDocument();
  });

  test('saves user to localStorage and navigates on successful registration', async () => {
    render(<RegisterPage />);

    // Preenchendo o formulário corretamente
    fireEvent.change(screen.getByLabelText(/nome/i), { target: { value: 'Test User' } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@test.com' } });
    
    // CORREÇÃO CRÍTICA AQUI:
    fireEvent.change(screen.getByLabelText(/^senha$/i), { target: { value: 'senha123' } });
    fireEvent.change(screen.getByLabelText(/confirmar senha/i), { target: { value: 'senha123' } });

    // Submetendo
    fireEvent.click(screen.getByRole('button', { name: /criar conta/i }));

    // Verificações
    await waitFor(() => {
      // Verifica se salvou no localStorage
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'testUser',
        JSON.stringify({
          name: 'Test User',
          email: 'test@test.com',
          password: 'senha123'
        })
      );
      
      // Verifica se navegou para o login
      expect(mockNavigate).toHaveBeenCalledWith('/login');
    });
  });
});