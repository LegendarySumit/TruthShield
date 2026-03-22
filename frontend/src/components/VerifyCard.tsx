
import { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import ResultCard from './ResultCard';
import type { PredictionResult } from '../types';
import { ArrowPathIcon, DocumentTextIcon, ExclamationTriangleIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { trackEvent } from '../lib/analytics';

declare global {
  interface Window {
    turnstile?: {
      render: (
        container: string | HTMLElement,
        options: {
          sitekey: string;
          callback?: (token: string) => void;
          'expired-callback'?: () => void;
          'error-callback'?: () => void;
          theme?: 'light' | 'dark' | 'auto';
          size?: 'normal' | 'compact' | 'flexible';
        }
      ) => string;
      reset: (widgetId?: string) => void;
      remove: (widgetId?: string) => void;
    };
  }
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const REQUEST_TIMEOUT_MS = Number(import.meta.env.VITE_REQUEST_TIMEOUT_MS || 12000);
const TURNSTILE_SITE_KEY = import.meta.env.VITE_TURNSTILE_SITE_KEY || '';
const CAPTCHA_BYPASS = import.meta.env.VITE_CAPTCHA_BYPASS === 'true';
const CAPTCHA_ENABLED = Boolean(TURNSTILE_SITE_KEY) && import.meta.env.MODE !== 'test' && !CAPTCHA_BYPASS;

const ensureTurnstileScript = (): Promise<void> => {
  if (window.turnstile) {
    return Promise.resolve();
  }

  return new Promise((resolve, reject) => {
    const existingScript = document.querySelector<HTMLScriptElement>('script[data-turnstile-script="true"]');
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve(), { once: true });
      existingScript.addEventListener('error', () => reject(new Error('Failed to load Turnstile script')), { once: true });
      return;
    }

    const script = document.createElement('script');
    script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit';
    script.async = true;
    script.defer = true;
    script.dataset.turnstileScript = 'true';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Turnstile script'));
    document.head.appendChild(script);
  });
};

const VerifyCard = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [charCount, setCharCount] = useState(0);
  const [captchaToken, setCaptchaToken] = useState<string | null>(null);
  const [captchaLoading, setCaptchaLoading] = useState(false);
  const [showCaptchaWidget, setShowCaptchaWidget] = useState(true);
  const [captchaStatus, setCaptchaStatus] = useState<'idle' | 'verifying' | 'success'>('idle');
  const [retryPending, setRetryPending] = useState(false);
  const [requestTimedOut, setRequestTimedOut] = useState(false);
  const [requestAttempts, setRequestAttempts] = useState(0);

  const captchaContainerRef = useRef<HTMLDivElement | null>(null);
  const turnstileWidgetIdRef = useRef<string | null>(null);
  const verifyTimeoutRef = useRef<number | null>(null);
  const successTimeoutRef = useRef<number | null>(null);

  const submitRequest = async (payload: { text: string; captcha_token?: string }, isRetry = false) => {
    if (!navigator.onLine) {
      setError('You appear to be offline. Reconnect and try again.');
      setRetryPending(true);
      trackEvent('analysis_failed_offline', { attempt: requestAttempts + 1 });
      return;
    }

    setLoading(true);
    setResult(null);
    setError(null);
    setRequestTimedOut(false);
    setRetryPending(false);
    setRequestAttempts((prev) => prev + 1);

    trackEvent('analysis_request_started', {
      retry: isRetry,
      text_length: payload.text.length,
      captcha_enabled: CAPTCHA_ENABLED,
      timeout_ms: REQUEST_TIMEOUT_MS,
    });

    try {
      const response = await axios.post(`${API_URL}/api/v1/predict`, payload, { timeout: REQUEST_TIMEOUT_MS });
      setResult(response.data);
      trackEvent('analysis_request_succeeded', {
        retry: isRetry,
        prediction: response.data?.prediction || 'unknown',
      });
    } catch (err: unknown) {
      const axiosErr = err as {
        code?: string;
        response?: { data?: { error?: string; message?: string } };
        request?: unknown;
      };

      if (axiosErr.code === 'ECONNABORTED') {
        setRequestTimedOut(true);
        setRetryPending(true);
        setError(`Request timed out after ${Math.round(REQUEST_TIMEOUT_MS / 1000)}s. You can retry.`);
        trackEvent('analysis_failed_timeout', {
          timeout_ms: REQUEST_TIMEOUT_MS,
          retry: isRetry,
        });
      } else if (axiosErr.response) {
        const apiError = axiosErr.response.data?.error;
        const apiMessage = axiosErr.response.data?.message || 'Unable to analyze text';
        setError(`Server error: ${apiMessage}`);
        setRetryPending(true);
        trackEvent('analysis_failed_api', { error_code: apiError || 'unknown', retry: isRetry });

        if (apiError === 'captcha_required' || apiError === 'captcha_failed') {
          setCaptchaToken(null);
          setCaptchaStatus('idle');
          setShowCaptchaWidget(true);
          if (window.turnstile && turnstileWidgetIdRef.current) {
            window.turnstile.remove(turnstileWidgetIdRef.current);
            turnstileWidgetIdRef.current = null;
          }
        }
      } else if (axiosErr.request) {
        setError('Cannot connect to server. Please make sure the backend is running.');
        setRetryPending(true);
        trackEvent('analysis_failed_network', { retry: isRetry });
      } else {
        setError('An unexpected error occurred. Please try again.');
        setRetryPending(true);
        trackEvent('analysis_failed_unexpected', { retry: isRetry });
      }
      console.error('Error details:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!CAPTCHA_ENABLED || !showCaptchaWidget || !captchaContainerRef.current) {
      return;
    }

    let cancelled = false;
    setCaptchaLoading(true);

    ensureTurnstileScript()
      .then(() => {
        if (cancelled || !captchaContainerRef.current || !window.turnstile) {
          return;
        }

        if (turnstileWidgetIdRef.current) {
          window.turnstile.remove(turnstileWidgetIdRef.current);
          turnstileWidgetIdRef.current = null;
        }

        turnstileWidgetIdRef.current = window.turnstile.render(captchaContainerRef.current, {
          sitekey: TURNSTILE_SITE_KEY,
          theme: 'auto',
          size: 'normal',
          callback: (token: string) => {
            setCaptchaStatus('verifying');
            setError(null);

            verifyTimeoutRef.current = window.setTimeout(() => {
              setCaptchaStatus('success');
            }, 700);

            successTimeoutRef.current = window.setTimeout(() => {
              setCaptchaToken(token);
              setShowCaptchaWidget(false);
              if (window.turnstile && turnstileWidgetIdRef.current) {
                window.turnstile.remove(turnstileWidgetIdRef.current);
                turnstileWidgetIdRef.current = null;
              }
            }, 1800);
          },
          'expired-callback': () => {
            setCaptchaToken(null);
            setCaptchaStatus('idle');
            setShowCaptchaWidget(true);
            setError('Captcha expired. Please verify again before analyzing.');
          },
          'error-callback': () => {
            setCaptchaToken(null);
            setCaptchaStatus('idle');
            setShowCaptchaWidget(true);
            setError('Captcha failed. Please retry.');
          },
        });
      })
      .catch(() => {
        if (!cancelled) {
          setError('Unable to load captcha. Check your network and retry.');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setCaptchaLoading(false);
        }
      });

    return () => {
      cancelled = true;
      if (verifyTimeoutRef.current) {
        window.clearTimeout(verifyTimeoutRef.current);
        verifyTimeoutRef.current = null;
      }
      if (successTimeoutRef.current) {
        window.clearTimeout(successTimeoutRef.current);
        successTimeoutRef.current = null;
      }
    };
  }, [showCaptchaWidget]);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value;
    setText(newText);
    setCharCount(newText.length);
    if (error) setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter some text to analyze.');
      return;
    }

    if (text.trim().length < 50) {
      setError('Please enter at least 50 characters for accurate analysis.');
      return;
    }

    if (CAPTCHA_ENABLED && !captchaToken) {
      setError('Please complete captcha verification before analysis.');
      return;
    }

    const payload: { text: string; captcha_token?: string } = { text };
    if (CAPTCHA_ENABLED && captchaToken) {
      payload.captcha_token = captchaToken;
    }

    await submitRequest(payload, false);
  };

  const handleRetry = async () => {
    const payload: { text: string; captcha_token?: string } = { text };
    if (CAPTCHA_ENABLED && captchaToken) {
      payload.captcha_token = captchaToken;
    }

    trackEvent('analysis_retry_clicked', {
      prior_timeout: requestTimedOut,
      attempts: requestAttempts,
    });
    await submitRequest(payload, true);
  };

  return (
    <div className="max-w-4xl mx-auto p-2 xs:p-3 sm:p-6 lg:p-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative"
      >
        {/* Glowing border effect */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-violet-500 rounded-2xl blur opacity-10 group-hover:opacity-30 transition duration-1000"></div>
        
        <div className="relative bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-2xl shadow-2xl p-4 xs:p-5 sm:p-6 md:p-8 border border-purple-200 dark:border-indigo-900/50">
          <form onSubmit={handleSubmit}>
            {/* Header */}
            <div className="text-center mb-4 xs:mb-5 sm:mb-6">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200 }}
                className="inline-flex items-center justify-center w-10 h-10 xs:w-11 xs:h-11 sm:w-13 sm:h-13 md:w-16 md:h-16 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 mb-2.5 xs:mb-3 sm:mb-4 shadow-lg shadow-purple-500/30"
              >
                <DocumentTextIcon className="h-5 w-5 xs:h-5.5 xs:w-5.5 sm:h-6 sm:w-6 md:h-8 md:w-8 text-white" />
              </motion.div>
              <h2 className="text-lg xs:text-xl sm:text-2xl md:text-3xl font-black bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 dark:from-indigo-400 dark:via-purple-400 dark:to-violet-400 text-transparent bg-clip-text mb-1 sm:mb-2 leading-tight">
                Analyze News Article
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-xs xs:text-sm max-w-xs xs:max-w-sm sm:max-w-none mx-auto leading-relaxed">
                Paste any news article below and let our AI verify its authenticity
              </p>
            </div>

            {/* Textarea with enhanced styling */}
            <div className="relative group">
              <textarea
                value={text}
                onChange={handleTextChange}
                placeholder="📰 Paste your news article here... (minimum 50 characters)"
                className="relative w-full h-36 xs:h-40 sm:h-48 md:h-56 p-3 xs:p-3.5 sm:p-4 md:p-5 border-2 border-gray-200 dark:border-gray-700 rounded-xl bg-white/50 dark:bg-gray-800/50 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:border-indigo-500 dark:focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/15 focus:outline-none transition-all duration-300 resize-none backdrop-blur-sm font-medium text-sm sm:text-base"
                style={{ 
                  backgroundImage: 'linear-gradient(to right, rgba(99, 102, 241, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(99, 102, 241, 0.05) 1px, transparent 1px)',
                  backgroundSize: '20px 20px'
                }}
              />
              
              {/* Character count */}
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: text.length > 0 ? 1 : 0 }}
                className="absolute bottom-3 right-3 text-xs font-semibold text-gray-500 dark:text-gray-400 bg-white/80 dark:bg-gray-800/80 px-3 py-1 rounded-full backdrop-blur-sm"
              >
                {charCount} characters
              </motion.div>
            </div>

            {/* Error message */}
            <AnimatePresence>
              {error && !retryPending && (
                <motion.p
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  className="text-red-500 dark:text-red-400 text-sm mt-3 font-medium flex items-center"
                >
                  <span className="mr-2">⚠️</span> {error}
                </motion.p>
              )}
            </AnimatePresence>

            {retryPending && !loading && (
              <motion.div
                initial={{ opacity: 0, y: -8 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-3 rounded-xl border border-indigo-200/70 dark:border-indigo-800/60 bg-gradient-to-r from-indigo-50/85 via-white/70 to-violet-50/85 dark:from-indigo-950/45 dark:via-gray-900/55 dark:to-violet-950/40 px-3 sm:px-4 py-3"
              >
                <div className="flex flex-col sm:flex-row items-start sm:items-center sm:justify-between gap-3">
                  <div className="flex items-start gap-2.5">
                    <div className="mt-0.5 p-1.5 rounded-lg bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-300">
                      <ExclamationTriangleIcon className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-rose-500 dark:text-rose-300 leading-tight">
                        {error || 'Request failed. Please retry.'}
                      </p>
                      <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {requestTimedOut
                          ? 'The server took too long to respond. You can retry now.'
                          : 'Temporary issue detected. Retry to continue analysis.'}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 self-end sm:self-auto">
                    <button
                      type="button"
                      onClick={() => void handleRetry()}
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 text-white text-sm font-semibold shadow-md shadow-indigo-500/25 hover:opacity-95 transition-all"
                    >
                      <ArrowPathIcon className="h-4 w-4" />
                      {requestTimedOut ? 'Retry Timed-out Request' : 'Retry Request'}
                    </button>
                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400 bg-white/70 dark:bg-gray-800/70 px-2.5 py-1 rounded-md border border-gray-200 dark:border-gray-700">
                      Attempt #{requestAttempts + 1}
                    </span>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Submit button */}
            <div className="text-center mt-4 xs:mt-5 sm:mt-6">
              {CAPTCHA_ENABLED && showCaptchaWidget && (
                <div className="mb-4 flex flex-col items-center gap-2">
                  {captchaLoading ? <div className="h-[78px]" /> : <div ref={captchaContainerRef} />}
                  {captchaStatus === 'verifying' && (
                    <p className="text-xs sm:text-sm text-blue-400">Verifying...</p>
                  )}
                  {captchaStatus === 'success' && (
                    <p className="text-xs sm:text-sm text-green-400">Success. Continuing...</p>
                  )}
                </div>
              )}
              <motion.button
                type="submit"
                disabled={loading}
                whileHover={{ scale: loading ? 1 : 1.02 }}
                whileTap={{ scale: loading ? 1 : 0.98 }}
                className={`relative px-5 py-2.5 xs:px-6 xs:py-3 sm:px-8 sm:py-3.5 md:px-10 md:py-4 rounded-lg sm:rounded-xl font-bold text-xs xs:text-sm sm:text-base md:text-lg text-white shadow-md transition-all duration-300 ${
                  loading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 opacity-90 hover:opacity-100'
                }`}
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg
                      className="animate-spin h-5 w-5 sm:h-6 sm:w-6 mr-2 sm:mr-3 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12" cy="12" r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                      />
                    </svg>
                    Analyzing...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    <SparklesIcon className="h-5 w-5 sm:h-6 sm:w-6 mr-1.5 sm:mr-2" />
                    Verify Now
                  </span>
                )}
              </motion.button>
            </div>

            {/* Quick examples */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="mt-6 text-center"
            >
              <p className="text-xs text-gray-500 dark:text-gray-400 mb-2">Try with:</p>
              <div className="flex flex-wrap gap-2 justify-center">
                {['Real News', 'Breaking News', 'Viral Story'].map((label, idx) => (
                  <motion.button
                    key={idx}
                    type="button"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => {
                      const examples = [
                        'The Federal Reserve announced today a quarter-point increase in interest rates, citing concerns about inflation.',
                        'BREAKING: Scientists discover miracle cure! Doctors SHOCKED by this one weird trick!',
                        'Viral post claims famous celebrity is secretly an alien. Share before they delete this!'
                      ];
                      setText(examples[idx]);
                      setCharCount(examples[idx].length);
                    }}
                    className="px-3 py-1 text-xs rounded-full bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 text-purple-700 dark:text-purple-300 font-medium hover:shadow-md transition-all"
                  >
                    {label}
                  </motion.button>
                ))}
              </div>
            </motion.div>
          </form>
        </div>
      </motion.div>

      <AnimatePresence mode="wait">
        {result && <ResultCard result={result} />}
      </AnimatePresence>
    </div>
  );
};

export default VerifyCard;
