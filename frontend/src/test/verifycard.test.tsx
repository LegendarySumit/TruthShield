import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi, describe, it, beforeEach, expect } from 'vitest';
import VerifyCard from '../components/VerifyCard';
import axios from 'axios';

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
  },
}));

vi.mock('../lib/analytics', () => ({
  trackEvent: vi.fn(),
}));

const mockedAxios = axios as unknown as { post: ReturnType<typeof vi.fn> };

const buildValidText = () => 'This is a sufficiently long sample article body for reliable test execution and request validation.';

describe('VerifyCard request states', () => {
  beforeEach(() => {
    mockedAxios.post.mockReset();
  });

  it('shows loading state while request is in flight', async () => {
    let resolvePromise: ((value: unknown) => void) | undefined;
    mockedAxios.post.mockImplementation(
      () =>
        new Promise((resolve) => {
          resolvePromise = resolve;
        }),
    );

    render(<VerifyCard />);

    fireEvent.change(screen.getByPlaceholderText(/paste your news article/i), {
      target: { value: buildValidText() },
    });
    fireEvent.click(screen.getByRole('button', { name: /verify now/i }));

    expect(await screen.findByText(/analyzing/i)).toBeInTheDocument();

    resolvePromise?.({
      data: {
        prediction: 'Real',
        confidence: 0.89,
        explanation: 'Looks consistent',
        model_version: 'v3',
      },
    });

    await waitFor(() => expect(screen.getByText(/verification result/i)).toBeInTheDocument());
  });

  it('shows timeout error and retry action', async () => {
    mockedAxios.post.mockRejectedValue({ code: 'ECONNABORTED' });

    render(<VerifyCard />);

    fireEvent.change(screen.getByPlaceholderText(/paste your news article/i), {
      target: { value: buildValidText() },
    });
    fireEvent.click(screen.getByRole('button', { name: /verify now/i }));

    expect(await screen.findByText(/request timed out/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry timed-out request/i })).toBeInTheDocument();
  });

  it('shows server error message from API response', async () => {
    mockedAxios.post.mockRejectedValue({
      response: {
        data: {
          error: 'validation_error',
          message: 'Request validation failed.',
        },
      },
    });

    render(<VerifyCard />);

    fireEvent.change(screen.getByPlaceholderText(/paste your news article/i), {
      target: { value: buildValidText() },
    });
    fireEvent.click(screen.getByRole('button', { name: /verify now/i }));

    expect(await screen.findByText(/server error: request validation failed/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry request/i })).toBeInTheDocument();
  });

  it('shows network connectivity error when no response is received', async () => {
    mockedAxios.post.mockRejectedValue({ request: {} });

    render(<VerifyCard />);

    fireEvent.change(screen.getByPlaceholderText(/paste your news article/i), {
      target: { value: buildValidText() },
    });
    fireEvent.click(screen.getByRole('button', { name: /verify now/i }));

    expect(await screen.findByText(/cannot connect to server/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /retry request/i })).toBeInTheDocument();
  });
});
