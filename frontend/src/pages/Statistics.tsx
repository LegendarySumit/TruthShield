import React from 'react';
import { ShieldCheckIcon, ChartBarIcon, AcademicCapIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import Footer from '../components/Footer';

const Statistics: React.FC = () => {
  const stats = [
    { label: 'Detection Accuracy', value: '100%', icon: ShieldCheckIcon, color: 'from-green-400 to-emerald-500' },
    { label: 'Articles Analyzed', value: '800+', icon: ChartBarIcon, color: 'from-blue-400 to-cyan-500' },
    { label: 'Training Samples', value: '640', icon: AcademicCapIcon, color: 'from-purple-400 to-pink-500' },
    { label: 'Features Extracted', value: '1,360', icon: SparklesIcon, color: 'from-orange-400 to-red-500' },
  ];

  const modelDetails = [
    { label: 'Algorithm', value: 'Logistic Regression' },
    { label: 'Vectorization', value: 'TF-IDF with Bigrams' },
    { label: 'Precision', value: '100%' },
    { label: 'Recall', value: '100%' },
    { label: 'F1 Score', value: '1.0000' },
    { label: 'Test Set Size', value: '160 articles' },
  ];

  return (
    <div className="min-h-screen pt-20 pb-16 px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto text-center mb-16"
      >
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 text-transparent bg-clip-text">
          Model Statistics
        </h1>
        <p className="text-xl text-gray-400">
          Real-time performance metrics and technical details
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-300 blur-xl -z-10"
              style={{ background: `linear-gradient(to right, var(--tw-gradient-stops))` }}
            />
            <div className="bg-white/80 dark:bg-gray-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 hover:border-purple-500/50 transition-all duration-300">
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${stat.color} p-2.5 mb-4`}>
                <stat.icon className="w-full h-full text-white" />
              </div>
              <div className="text-4xl font-bold text-gray-900 dark:text-white mb-2">{stat.value}</div>
              <div className="text-gray-600 dark:text-gray-400 text-sm">{stat.label}</div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Model Details */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="max-w-4xl mx-auto"
      >
        <div className="bg-white/80 dark:bg-gray-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-8">
          <h2 className="text-3xl font-bold mb-6 text-gray-900 dark:text-white">Technical Specifications</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {modelDetails.map((detail, index) => (
              <motion.div
                key={detail.label}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.6 + index * 0.1 }}
                className="flex justify-between items-center p-4 bg-gray-100/50 dark:bg-gray-800/50 rounded-xl border border-gray-300/50 dark:border-gray-700/50"
              >
                <span className="text-gray-600 dark:text-gray-400">{detail.label}</span>
                <span className="text-gray-900 dark:text-white font-semibold">{detail.value}</span>
              </motion.div>
            ))}
          </div>

          {/* Training Details */}
          <div className="mt-8 p-6 bg-gradient-to-r from-purple-100/50 to-pink-100/50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl border border-purple-500/20">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Training Configuration</h3>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-start">
                <span className="text-purple-500 dark:text-purple-400 mr-2">•</span>
                <span>Enhanced text preprocessing: lowercase, URL removal, punctuation cleaning</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-500 dark:text-purple-400 mr-2">•</span>
                <span>TF-IDF vectorization with bigrams (n-gram range: 1-2)</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-500 dark:text-purple-400 mr-2">•</span>
                <span>Balanced class weights for optimal performance</span>
              </li>
              <li className="flex items-start">
                <span className="text-purple-500 dark:text-purple-400 mr-2">•</span>
                <span>80/20 train-test split with stratification</span>
              </li>
            </ul>
          </div>
        </div>
      </motion.div>
      <Footer />
    </div>
  );
};

export default Statistics;
