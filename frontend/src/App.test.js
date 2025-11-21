import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// NÃO precisamos fazer mock do react-router-dom aqui, 
// pois o App.js já contém o <Router> real.

test('renders Quiz Game title', () => {
  render(<App />);
  
  // Procura pelo título "Quiz Game" que está na Landing Page
  const titleElement = screen.getByText(/quiz game/i);
  expect(titleElement).toBeInTheDocument();
});