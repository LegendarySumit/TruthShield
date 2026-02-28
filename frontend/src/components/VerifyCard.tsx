
import { useState } from 'react';
import axios from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import ResultCard from './ResultCard';
import type { PredictionResult } from '../types';
import { DocumentTextIcon, SparklesIcon } from '@heroicons/react/24/outline';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const VerifyCard = () => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [charCount, setCharCount] = useState(0);

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

    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, { text });
      setResult(response.data);
    } catch (err: any) {
      if (err.response) {
        // Server responded with error
        setError(`Server error: ${err.response.data.detail || 'Unable to analyze text'}`);
      } else if (err.request) {
        // Request made but no response
        setError('Cannot connect to server. Please make sure the backend is running.');
      } else {
        // Something else went wrong
        setError('An unexpected error occurred. Please try again.');
      }
      console.error('Error details:', err);
    } finally {
      setLoading(false);
    }
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
              {error && (
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

            {/* Submit button */}
            <div className="text-center mt-4 xs:mt-5 sm:mt-6">
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
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="mr-2 sm:mr-3"
                    >
                      <SparklesIcon className="h-5 w-5 sm:h-6 sm:w-6" />
                    </motion.div>
                    Analyzing Magic...
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
