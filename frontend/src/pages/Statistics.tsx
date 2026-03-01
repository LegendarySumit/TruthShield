import { ShieldCheckIcon, ChartBarIcon, AcademicCapIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';
import Footer from '../components/Footer';

const Statistics = () => {
  const stats = [
    { label: 'Detection Accuracy', value: '99.92%', icon: ShieldCheckIcon, color: 'from-green-400 to-emerald-500' },
    { label: 'Training Samples', value: '20K+', icon: ChartBarIcon, color: 'from-blue-400 to-cyan-500' },
    { label: 'Training Size (Train set)', value: '16,000', icon: AcademicCapIcon, color: 'from-indigo-400 to-purple-500' },
    { label: 'Features Extracted', value: '10,000', icon: SparklesIcon, color: 'from-purple-400 to-violet-500' },
  ];

  const modelDetails = [
    { label: 'Algorithm', value: 'LR + SVM + Random Forest' },
    { label: 'Vectorization', value: 'TF-IDF with Bigrams' },
    { label: 'Precision', value: '~99.9%' },
    { label: 'Recall', value: '~99.9%' },
    { label: 'F1 Score', value: '0.9992' },
    { label: 'Test Set Size', value: '4,000 samples' },
  ];

  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-1 pt-16 sm:pt-18 md:pt-20 pb-10 sm:pb-12 md:pb-16 px-3 xs:px-4">
        {/* Header */}
        <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl mx-auto text-center mb-8 sm:mb-12 md:mb-16"
      >
        <h1 className="text-3xl xs:text-4xl sm:text-4xl md:text-5xl font-bold mb-3 sm:mb-4 md:mb-6 bg-gradient-to-r from-indigo-400 via-purple-500 to-violet-500 text-transparent bg-clip-text">
          Model Statistics
        </h1>
        <p className="text-base sm:text-lg md:text-xl text-gray-400">
          Real-time performance metrics and technical details
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="max-w-6xl mx-auto grid grid-cols-2 lg:grid-cols-4 gap-3 xs:gap-4 sm:gap-5 md:gap-6 mb-8 sm:mb-12 md:mb-16 px-1 xs:px-0">
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
            <div className="h-full bg-white/80 dark:bg-gray-950/50 backdrop-blur-xl border border-indigo-500/20 rounded-xl sm:rounded-2xl p-3.5 xs:p-4 sm:p-5 md:p-6 hover:border-indigo-500/50 transition-all duration-300 flex flex-col">
              <div className={`w-9 h-9 xs:w-10 xs:h-10 sm:w-11 sm:h-11 md:w-12 md:h-12 rounded-lg sm:rounded-xl bg-gradient-to-r ${stat.color} p-1.5 xs:p-2 sm:p-2 md:p-2.5 mb-2.5 sm:mb-3 md:mb-4`}>
                <stat.icon className="w-full h-full text-white" />
              </div>
              <div className="text-2xl xs:text-3xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-1 sm:mb-2">{stat.value}</div>
              <div className="text-gray-600 dark:text-gray-400 text-xs sm:text-sm mt-auto">{stat.label}</div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Model Details — Free-flow Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="max-w-6xl mx-auto"
      >
        {/* Section header */}
        <div className="mb-6 sm:mb-8 md:mb-10">
          <h2 className="text-2xl xs:text-3xl sm:text-3xl md:text-4xl font-black text-gray-900 dark:text-white tracking-tight mb-2 sm:mb-3">Technical Specifications</h2>
          <p className="text-gray-500 dark:text-gray-400 text-sm sm:text-base md:text-lg">Core model architecture and performance benchmarks</p>
          <div className="mt-4 h-px w-24 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
        </div>

        {/* Spec grid — full width, 3-column */}
        <div className="grid grid-cols-1 xs:grid-cols-2 lg:grid-cols-3 gap-2.5 xs:gap-3 sm:gap-4 mb-8 sm:mb-10 md:mb-12">
          {modelDetails.map((detail, index) => (
            <motion.div
              key={detail.label}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 + index * 0.08 }}
              whileHover={{ y: -3 }}
              className="flex justify-between items-center p-3 xs:p-3.5 sm:p-4 md:p-5 bg-gray-50 dark:bg-gray-800/40 rounded-lg sm:rounded-xl border border-gray-200/80 dark:border-gray-700/30 hover:border-indigo-300 dark:hover:border-indigo-500/30 transition-all duration-300 group"
            >
              <span className="text-gray-500 dark:text-gray-400 text-xs sm:text-sm">{detail.label}</span>
              <span className="text-gray-900 dark:text-white font-bold text-xs sm:text-sm group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{detail.value}</span>
            </motion.div>
          ))}
        </div>

        {/* Divider */}
        <div className="h-px w-full bg-gradient-to-r from-transparent via-gray-300 dark:via-gray-700 to-transparent mb-8 sm:mb-10 md:mb-12"></div>

        {/* Training Configuration — centered layout */}
        <div className="text-center mb-6 sm:mb-8 md:mb-10">
          <h3 className="text-xl xs:text-2xl sm:text-2xl md:text-3xl font-black text-gray-900 dark:text-white tracking-tight mb-3 sm:mb-4">Training Configuration</h3>
          <p className="text-gray-500 dark:text-gray-400 text-sm sm:text-base leading-relaxed max-w-2xl mx-auto">
            Our detection model is built on a carefully crafted training pipeline. From cleaning raw news articles to producing a production-grade classifier, 
            every step is designed to maximize accuracy while maintaining balanced performance across both real and fake news categories.
          </p>
          <div className="mt-5 h-px w-20 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full mx-auto"></div>
        </div>

        {/* Steps — centered 2-column grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4 max-w-4xl mx-auto">
          {[
            { label: 'Text Preprocessing', desc: 'All input is lowercased, URLs are stripped, and punctuation is cleaned to normalize text before analysis.' },
            { label: 'Vectorization', desc: 'TF-IDF converts text into numerical features using unigrams and bigrams (n-gram range: 1-2) with up to 10,000 features.' },
            { label: 'Class Balancing', desc: 'Balanced class weights ensure the model doesn\'t favor either class — critical for unbiased fake news detection.' },
            { label: 'Data Split', desc: 'An 80/20 stratified train-test split preserves the real/fake ratio across both sets for reliable evaluation.' },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 + i * 0.08 }}
              whileHover={{ y: -3 }}
              className="flex items-start gap-3 sm:gap-4 p-3.5 xs:p-4 sm:p-5 md:p-6 rounded-lg sm:rounded-xl bg-gray-50 dark:bg-gray-800/30 border border-gray-200/80 dark:border-gray-700/30 hover:border-indigo-300 dark:hover:border-indigo-500/30 transition-all duration-300 group"
            >
              <div className="w-8 h-8 xs:w-9 xs:h-9 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl bg-indigo-100 dark:bg-indigo-500/10 flex items-center justify-center flex-shrink-0 mt-0.5 group-hover:scale-110 transition-transform">
                <span className="text-indigo-600 dark:text-indigo-400 text-xs font-bold">{String(i + 1).padStart(2, '0')}</span>
              </div>
              <div className="min-w-0">
                <div className="font-bold text-gray-900 dark:text-white text-sm sm:text-[15px] mb-0.5 sm:mb-1">{item.label}</div>
                <div className="text-gray-500 dark:text-gray-400 text-xs sm:text-sm leading-relaxed">{item.desc}</div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
      </div>
      <Footer />
    </div>
  );
};

export default Statistics;
