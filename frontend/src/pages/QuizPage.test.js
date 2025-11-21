import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import QuizPage from './QuizPage';
import '@testing-library/jest-dom';

// Mock do useNavigate
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

// Mock do sessionStorage - implementação completa e funcional
let sessionStore = {};

// Recria o mock do sessionStorage para garantir que funcione
const setupSessionStorageMock = () => {
  const mock = {
    getItem: jest.fn((key) => {
      return sessionStore[key] || null;
    }),
    setItem: jest.fn((key, value) => {
      sessionStore[key] = String(value);
    }),
    removeItem: jest.fn((key) => {
      delete sessionStore[key];
    }),
    clear: jest.fn(() => {
      sessionStore = {};
    }),
  };
  
  Object.defineProperty(window, 'sessionStorage', {
    value: mock,
    writable: true,
    configurable: true,
  });
  
  return mock;
};

// Configura o mock inicialmente
setupSessionStorageMock();

// Mock do Date.now
const mockDateNow = jest.fn(() => 1000000);
global.Date.now = mockDateNow;

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('QuizPage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    sessionStore = {}; // Limpa o store
    mockNavigate.mockClear();
    mockDateNow.mockReturnValue(1000000);
    // Recria o mock para garantir que funcione
    setupSessionStorageMock();
  });

  const mockQuizData = {
    quiz_id: 1,
    num_questions: 3
  };

  test('navigates to quiz-setup when no quiz data', () => {
    sessionStore = {}; // Garante que está vazio
    renderWithRouter(<QuizPage />);
    expect(mockNavigate).toHaveBeenCalledWith('/quiz-setup');
  });

  test('renders first question when quiz data exists', async () => {
    // Configura o sessionStorage ANTES de renderizar
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    
    // Garante que o getItem retorna o valor correto
    window.sessionStorage.getItem = jest.fn((key) => {
      if (key === 'currentQuiz') {
        return quizDataString;
      }
      return null;
    });
    
    renderWithRouter(<QuizPage />);
    
    // Aguarda o carregamento e renderização - timeout maior
    expect(await screen.findByText(/qual é a capital do brasil/i, {}, { timeout: 10000 })).toBeInTheDocument();
    expect(screen.getByText(/são paulo/i)).toBeInTheDocument();
    expect(screen.getByText(/rio de janeiro/i)).toBeInTheDocument();
  });

  test('displays progress bar', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    expect(await screen.findByText(/pergunta 1 de 3/i, {}, { timeout: 10000 })).toBeInTheDocument();
  });

  test('displays score', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    expect(await screen.findByText(/pontuação: 0/i, {}, { timeout: 10000 })).toBeInTheDocument();
  });

  test('selects answer when option is clicked', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    const option = await screen.findByText(/brasília/i, {}, { timeout: 10000 });
    fireEvent.click(option);
    
    expect(option).toHaveClass('selected');
  });

  test('submits answer and shows result', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    const correctOption = await screen.findByText(/brasília/i, {}, { timeout: 10000 });
    fireEvent.click(correctOption);
    
    const submitButton = await screen.findByRole('button', { name: /confirmar resposta/i }, { timeout: 5000 });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/correto/i)).toBeInTheDocument();
    }, { timeout: 5000 });
  });


  test('moves to next question after submitting', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    const correctOption = await screen.findByText(/brasília/i, {}, { timeout: 10000 });
    fireEvent.click(correctOption);
    
    const submitButton = await screen.findByRole('button', { name: /confirmar resposta/i }, { timeout: 5000 });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/correto/i)).toBeInTheDocument();
    }, { timeout: 5000 });
    
    const nextButton = await screen.findByRole('button', { name: /próxima pergunta/i }, { timeout: 5000 });
    fireEvent.click(nextButton);
    
    await waitFor(() => {
      expect(screen.getByText(/em que ano o brasil foi descoberto/i)).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  test('navigates to results when last question is answered', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    // Aguarda o carregamento inicial
    await screen.findByText(/qual é a capital do brasil/i, {}, { timeout: 10000 });

    // O componente cria 3 perguntas mockadas internamente
    const questions = [
      { correct_answer: 'Brasília' },
      { correct_answer: '1500' },
      { correct_answer: 'Júpiter' }
    ];

    for (let i = 0; i < questions.length; i++) {
      const question = questions[i];
      
      const correctOption = await screen.findByText(question.correct_answer, {}, { timeout: 5000 });
      fireEvent.click(correctOption);
      
      const submitButton = await screen.findByRole('button', { name: /confirmar resposta/i }, { timeout: 5000 });
      fireEvent.click(submitButton);
      
      await waitFor(() => {
        expect(screen.getByText(/correto/i)).toBeInTheDocument();
      }, { timeout: 5000 });
      
      if (i < questions.length - 1) {
        const nextButton = await screen.findByRole('button', { name: /próxima pergunta/i }, { timeout: 5000 });
        fireEvent.click(nextButton);
        
        // Aguarda a próxima pergunta aparecer
        await waitFor(() => {
          expect(screen.queryByText(/correto/i)).not.toBeInTheDocument();
        }, { timeout: 5000 });
      } else {
        const finishButton = await screen.findByRole('button', { name: /ver resultados/i }, { timeout: 5000 });
        fireEvent.click(finishButton);
      }
    }
    
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/results');
    }, { timeout: 5000 });
  });

  test('disables answer selection after submission', async () => {
    const quizDataString = JSON.stringify(mockQuizData);
    sessionStore['currentQuiz'] = quizDataString;
    window.sessionStorage.getItem = jest.fn((key) => key === 'currentQuiz' ? quizDataString : null);
    
    renderWithRouter(<QuizPage />);
    
    const option = await screen.findByText(/brasília/i, {}, { timeout: 10000 });
    fireEvent.click(option);
    
    const submitButton = await screen.findByRole('button', { name: /confirmar resposta/i }, { timeout: 5000 });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(option).toBeDisabled();
    }, { timeout: 5000 });
  });
});
