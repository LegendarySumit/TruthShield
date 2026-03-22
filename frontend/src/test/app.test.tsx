import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App', () => {
  it('renders core homepage heading and analysis section', () => {
    render(<App />);
    expect(screen.getByText(/Unmask the Truth/i)).toBeInTheDocument();
    expect(screen.getByText(/Analyze News Article/i)).toBeInTheDocument();
  });
});
