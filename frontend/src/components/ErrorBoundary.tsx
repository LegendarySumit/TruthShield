import { Component, type ErrorInfo, type ReactNode } from 'react';
import { trackEvent } from '../lib/analytics';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = { hasError: false };

  public static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    trackEvent('ui_error_boundary_triggered', {
      message: error.message,
      stack_length: (errorInfo.componentStack || '').length,
    });
  }

  public render(): ReactNode {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center p-6 bg-gray-50 dark:bg-gray-900">
          <div className="max-w-md w-full rounded-2xl border border-red-200 dark:border-red-900 bg-white/90 dark:bg-gray-950/80 p-6 text-center shadow-xl">
            <h1 className="text-xl font-bold text-red-600 dark:text-red-400">Something went wrong</h1>
            <p className="mt-3 text-sm text-gray-600 dark:text-gray-300">
              The app hit an unexpected error. Please refresh the page.
            </p>
            <button
              type="button"
              onClick={() => window.location.reload()}
              className="mt-5 px-4 py-2 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700 transition-colors"
            >
              Reload App
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
