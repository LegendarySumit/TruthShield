
import { useState } from 'react';
import axios from 'axios';
import { AnimatePresence, motion } from 'framer-motion';
import ResultCard from './ResultCard';
import type { PredictionResult } from '../types';
import { DocumentTextIcon, SparklesIcon } from '@heroicons/react/24/outline';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
        setError('Cannot connect to server. Please make sure the backend is running on http://localhost:8000');
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
    <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative"
      >
        {/* Glowing border effect */}
        <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 rounded-2xl blur opacity-30 group-hover:opacity-100 transition duration-1000"></div>
        
        <div className="relative bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-purple-200 dark:border-purple-800">
          <form onSubmit={handleSubmit}>
            {/* Header */}
            <div className="text-center mb-6">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200 }}
                className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 mb-4 shadow-lg shadow-purple-500/50"
              >
                <DocumentTextIcon className="h-8 w-8 text-white" />
              </motion.div>
              <h2 className="text-3xl font-black bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 dark:from-purple-400 dark:via-pink-400 dark:to-red-400 text-transparent bg-clip-text mb-2">
                Analyze News Article
              </h2>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Paste any news article below and let our AI verify its authenticity
              </p>
            </div>

            {/* Textarea with enhanced styling */}
            <div className="relative group">
              <motion.div
                animate={text.length > 0 ? { opacity: 1, scale: 1 } : { opacity: 0, scale: 0.95 }}
                className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-pink-600 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-500"
              ></motion.div>
              
              <textarea
                value={text}
                onChange={handleTextChange}
                placeholder="📰 Paste your news article here... (minimum 50 characters)"
                className="relative w-full h-56 p-5 border-2 border-gray-200 dark:border-gray-700 rounded-xl bg-white/50 dark:bg-gray-800/50 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:border-purple-500 dark:focus:border-purple-500 focus:ring-4 focus:ring-purple-500/20 focus:outline-none transition-all duration-300 resize-none backdrop-blur-sm font-medium"
                style={{ 
                  backgroundImage: 'linear-gradient(to right, rgba(168, 85, 247, 0.05) 1px, transparent 1px), linear-gradient(to bottom, rgba(168, 85, 247, 0.05) 1px, transparent 1px)',
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
            <div className="text-center mt-6">
              <motion.button
                type="submit"
                disabled={loading}
                whileHover={{ scale: loading ? 1 : 1.05 }}
                whileTap={{ scale: loading ? 1 : 0.95 }}
                className={`relative px-12 py-4 rounded-xl font-bold text-lg text-white shadow-xl transition-all duration-300 ${
                  loading
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 hover:shadow-2xl hover:shadow-purple-500/50'
                }`}
              >
                {loading ? (
                  <span className="flex items-center">
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                      className="mr-3"
                    >
                      <SparklesIcon className="h-6 w-6" />
                    </motion.div>
                    Analyzing Magic...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    <SparklesIcon className="h-6 w-6 mr-2" />
                    Verify Now
                  </span>
                )}
                
                {!loading && (
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="absolute inset-0 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 rounded-xl blur-xl opacity-50"
                  />
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
