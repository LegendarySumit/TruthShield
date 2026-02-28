
import { motion } from 'framer-motion';
import type { PredictionResult } from '../types';
import { CheckCircleIcon, XCircleIcon, ShieldCheckIcon, ExclamationTriangleIcon } from '@heroicons/react/24/solid';
import { SparklesIcon } from '@heroicons/react/24/outline';

interface ResultCardProps {
  result: PredictionResult;
}

const ResultCard = ({ result }: ResultCardProps) => {
  const isReal = result.prediction === 'Real';
  const confidencePercent = (result.confidence * 100).toFixed(1);
  const confidence = result.confidence;

  // Determine confidence level
  const getConfidenceLevel = () => {
    if (confidence >= 0.9) return { text: 'Very High', color: 'emerald' };
    if (confidence >= 0.75) return { text: 'High', color: 'green' };
    if (confidence >= 0.6) return { text: 'Moderate', color: 'yellow' };
    return { text: 'Low', color: 'orange' };
  };

  const confidenceLevel = getConfidenceLevel();

  return (
    <motion.div
      initial={{ opacity: 0, y: 50, scale: 0.9 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -50, scale: 0.9 }}
      transition={{ duration: 0.6, type: 'spring' }}
      className="mt-10"
    >
      {/* Glowing border */}
      <div className="relative">
        <motion.div
          animate={{
            opacity: [0.2, 0.35, 0.2],
          }}
          transition={{ duration: 3, repeat: Infinity }}
          className={`absolute -inset-0.5 rounded-3xl blur-lg ${
            isReal
              ? 'bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 opacity-30'
              : 'bg-gradient-to-r from-red-600 via-rose-600 to-slate-600 opacity-25'
          }`}
        />

        <div className={`relative rounded-3xl p-4 xs:p-5 sm:p-6 md:p-8 shadow-2xl backdrop-blur-xl border-2 ${
          isReal
            ? 'bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 border-green-200 dark:border-green-800/50'
            : 'bg-gradient-to-br from-red-50 to-rose-50 dark:from-red-900/30 dark:to-rose-900/30 border-red-200 dark:border-red-800/50'
        }`}>
          
          {/* Header Section */}
          <div className="flex flex-col xs:flex-row items-start xs:justify-between gap-3 xs:gap-4 mb-4 sm:mb-6">
            <div className="flex items-center space-x-2.5 xs:space-x-3 sm:space-x-4">
              <motion.div
                initial={{ scale: 0, rotate: -180 }}
                animate={{ scale: 1, rotate: 0 }}
                transition={{ type: 'spring', stiffness: 200, delay: 0.2 }}
                className={`p-2 xs:p-2.5 sm:p-3 md:p-4 rounded-xl sm:rounded-2xl ${
                  isReal
                    ? 'bg-gradient-to-br from-green-500 to-emerald-500 shadow-lg shadow-green-500/30'
                    : 'bg-gradient-to-br from-red-600 to-rose-600 shadow-lg shadow-red-500/30'
                }`}
              >
                {isReal ? (
                  <ShieldCheckIcon className="h-6 w-6 xs:h-7 xs:w-7 sm:h-8 sm:w-8 md:h-10 md:w-10 text-white" />
                ) : (
                  <ExclamationTriangleIcon className="h-6 w-6 xs:h-7 xs:w-7 sm:h-8 sm:w-8 md:h-10 md:w-10 text-white" />
                )}
              </motion.div>

              <div>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  <p className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-1">
                    Verification Result
                  </p>
                  <h3 className={`text-2xl xs:text-3xl sm:text-3xl md:text-4xl font-black ${
                    isReal
                      ? 'bg-gradient-to-r from-green-500 to-emerald-500 dark:from-green-400 dark:to-emerald-400'
                      : 'bg-gradient-to-r from-red-500 to-rose-600 dark:from-red-400 dark:to-rose-400'
                  } text-transparent bg-clip-text`}>
                    {result.prediction}
                  </h3>
                </motion.div>
              </div>
            </div>

            {/* Confidence badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4, type: 'spring' }}
              className={`px-3 py-1.5 sm:px-4 sm:py-2 rounded-full bg-gradient-to-r ${
                confidenceLevel.color === 'emerald' ? 'from-emerald-500 to-teal-500' :
                confidenceLevel.color === 'green' ? 'from-green-500 to-emerald-500' :
                confidenceLevel.color === 'yellow' ? 'from-yellow-500 to-orange-500' :
                'from-orange-500 to-red-500'
              } text-white font-bold shadow-lg`}
            >
              <div className="flex items-center space-x-1">
                <SparklesIcon className="h-3.5 w-3.5 sm:h-4 sm:w-4" />
                <span className="text-xs sm:text-sm">{confidenceLevel.text}</span>
              </div>
            </motion.div>
          </div>

          {/* Confidence Progress Bar */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="mb-6"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
                Confidence Score
              </span>
              <span className={`text-lg xs:text-xl sm:text-2xl font-black ${
                isReal
                  ? 'text-green-600 dark:text-green-400'
                  : 'text-red-600 dark:text-red-400'
              }`}>
                {confidencePercent}%
              </span>
            </div>
            
            <div className="relative h-3 sm:h-4 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${confidencePercent}%` }}
                transition={{ duration: 1, delay: 0.6, ease: 'easeOut' }}
                className={`h-full rounded-full ${
                  isReal
                    ? 'bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500'
                    : 'bg-gradient-to-r from-red-500 via-pink-500 to-orange-500'
                }`}
              >
                <motion.div
                  animate={{ x: ['-100%', '100%'] }}
                  transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
                  className="h-full w-full bg-gradient-to-r from-transparent via-white/30 to-transparent"
                />
              </motion.div>
            </div>
          </motion.div>

          {/* Explanation Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className={`p-3 xs:p-4 sm:p-5 rounded-xl sm:rounded-2xl ${
              isReal
                ? 'bg-green-100/50 dark:bg-green-900/20 border-2 border-green-200 dark:border-green-800'
                : 'bg-red-100/50 dark:bg-red-900/20 border-2 border-red-200 dark:border-red-800'
            }`}
          >
            <div className="flex items-start space-x-3">
              <div className={`mt-1 p-1.5 sm:p-2 rounded-lg ${
                isReal ? 'bg-green-500' : 'bg-red-500'
              }`}>
                {isReal ? (
                  <CheckCircleIcon className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
                ) : (
                  <XCircleIcon className="h-4 w-4 sm:h-5 sm:w-5 text-white" />
                )}
              </div>
              <div>
                <h4 className="font-bold text-gray-900 dark:text-gray-100 mb-2">
                  AI Analysis
                </h4>
                <p className="text-sm sm:text-base text-gray-700 dark:text-gray-300 leading-relaxed">
                  {result.explanation}
                </p>
              </div>
            </div>
          </motion.div>

          {/* Action Tips */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.9 }}
            className="mt-6 pt-6 border-t-2 border-gray-200 dark:border-gray-700"
          >
            <p className="text-xs text-gray-600 dark:text-gray-400 text-center">
              {isReal
                ? '✅ This article appears to be legitimate. Always verify from multiple sources.'
                : '⚠️ Exercise caution with this content. Cross-reference with trusted news sources.'}
            </p>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultCard;
