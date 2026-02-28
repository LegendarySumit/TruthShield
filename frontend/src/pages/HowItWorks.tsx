import React from 'react';
import { motion } from 'framer-motion';
import { 
  DocumentTextIcon, 
  BeakerIcon, 
  ChartBarIcon, 
  ShieldCheckIcon,
  SparklesIcon,
  ClipboardDocumentCheckIcon
} from '@heroicons/react/24/outline';
import Footer from '../components/Footer';

const HowItWorks: React.FC = () => {
  const steps = [
    {
      icon: DocumentTextIcon,
      title: '1. Submit Your Text',
      description: 'Paste the news article, headline, or social media post you want to verify. Minimum 50 characters required for accurate analysis.',
      color: 'from-blue-400 to-cyan-500'
    },
    {
      icon: SparklesIcon,
      title: '2. Text Preprocessing',
      description: 'Our system cleans your text by removing URLs, special characters, and converting to lowercase. This ensures consistent analysis.',
      color: 'from-indigo-400 to-purple-500'
    },
    {
      icon: BeakerIcon,
      title: '3. Feature Extraction',
      description: 'TF-IDF (Term Frequency-Inverse Document Frequency) extracts 1,360 linguistic features including word patterns, bigrams, and statistical markers.',
      color: 'from-green-400 to-emerald-500'
    },
    {
      icon: ChartBarIcon,
      title: '4. ML Classification',
      description: 'Our Logistic Regression model analyzes extracted features against 800 training samples to identify patterns common in fake vs. real news.',
      color: 'from-purple-400 to-violet-500'
    },
    {
      icon: ShieldCheckIcon,
      title: '5. Confidence Calculation',
      description: 'The model generates a probability score (0-100%) indicating confidence in its prediction. Higher scores mean stronger certainty.',
      color: 'from-fuchsia-400 to-pink-500'
    },
    {
      icon: ClipboardDocumentCheckIcon,
      title: '6. Results & Explanation',
      description: 'Receive instant results with detailed explanation of linguistic markers, sentiment analysis, and credibility indicators found in your text.',
      color: 'from-indigo-400 to-purple-500'
    }
  ];

  const technicalDetails = [
    {
      title: 'Natural Language Processing',
      icon: '🧠',
      gradient: 'from-blue-500 to-cyan-500',
      accentBorder: 'border-blue-500/30 hover:border-blue-400/60',
      accentBg: 'bg-blue-500/10',
      accentText: 'text-blue-400',
      items: [
        'Tokenization and lemmatization',
        'Stop word removal (English)',
        'N-gram analysis (unigrams + bigrams)',
        'TF-IDF vectorization with 5000 max features'
      ]
    },
    {
      title: 'Machine Learning Model',
      icon: '⚙️',
      gradient: 'from-indigo-500 to-purple-500',
      accentBorder: 'border-indigo-500/30 hover:border-indigo-400/60',
      accentBg: 'bg-indigo-500/10',
      accentText: 'text-indigo-400',
      items: [
        'Algorithm: Logistic Regression',
        'Training samples: 640 balanced articles',
        'Test accuracy: 100% on 160 samples',
        'Regularization: L2 with balanced class weights'
      ]
    },
    {
      title: 'Fake News Indicators',
      icon: '🔍',
      gradient: 'from-violet-500 to-fuchsia-500',
      accentBorder: 'border-violet-500/30 hover:border-violet-400/60',
      accentBg: 'bg-violet-500/10',
      accentText: 'text-violet-400',
      items: [
        'Sensational language & clickbait',
        'Emotional manipulation patterns',
        'Lack of credible source attribution',
        'Unusual punctuation and capitalization'
      ]
    }
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
          How It Works
        </h1>
        <p className="text-base sm:text-lg md:text-xl text-gray-400">
          Discover the science behind fake news detection
        </p>
      </motion.div>

      {/* Process Steps */}
      <div className="max-w-6xl mx-auto mb-12 sm:mb-16 md:mb-20">
        {steps.map((step, index) => (
          <motion.div
            key={step.title}
            initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
            className="relative mb-6 sm:mb-8 md:mb-12 last:mb-0"
          >
            <div className="flex items-start gap-3 xs:gap-4 sm:gap-5 md:gap-6">
              {/* Icon */}
              <div className="flex-shrink-0">
                <div className={`w-10 h-10 xs:w-11 xs:h-11 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-xl sm:rounded-2xl bg-gradient-to-r ${step.color} p-2 sm:p-2.5 md:p-3 shadow-lg`}>
                  <step.icon className="w-full h-full text-white" />
                </div>
              </div>

              {/* Content */}
              <div className="flex-1 bg-white/80 dark:bg-gray-950/50 backdrop-blur-xl border border-indigo-500/20 rounded-xl sm:rounded-2xl p-3 xs:p-4 sm:p-5 md:p-6 hover:border-indigo-500/50 transition-all duration-300">
                <h3 className="text-base xs:text-lg sm:text-xl md:text-2xl font-bold text-gray-900 dark:text-white mb-1.5 sm:mb-2 md:mb-3">{step.title}</h3>
                <p className="text-sm sm:text-base text-gray-700 dark:text-gray-300 leading-relaxed">{step.description}</p>
              </div>
            </div>

            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className="absolute left-5 xs:left-[1.375rem] sm:left-7 md:left-8 top-14 sm:top-16 md:top-20 w-0.5 h-6 sm:h-8 md:h-12 bg-gradient-to-b from-indigo-500/50 to-transparent" />
            )}
          </motion.div>
        ))}
      </div>

      {/* Technical Details */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-6xl mx-auto"
      >
        <h2 className="text-2xl xs:text-3xl sm:text-3xl md:text-4xl font-black text-center mb-3 sm:mb-4 text-gray-900 dark:text-white tracking-tight">
          Technical Deep Dive
        </h2>
        <p className="text-center text-gray-500 dark:text-gray-400 mb-8 sm:mb-10 md:mb-14 text-sm sm:text-base md:text-lg max-w-2xl mx-auto">
          Under the hood — the science powering every prediction
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
          {technicalDetails.map((section, index) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15, type: 'spring', stiffness: 100 }}
              whileHover={{ y: -8 }}
              className={`relative group overflow-hidden bg-white dark:bg-[#0c0e24] rounded-xl sm:rounded-2xl p-4 xs:p-5 sm:p-6 md:p-8 border ${section.accentBorder} transition-all duration-500 shadow-lg hover:shadow-2xl dark:hover:shadow-indigo-500/5`}
            >
              {/* Top gradient strip */}
              <div className={`absolute top-0 inset-x-0 h-1 bg-gradient-to-r ${section.gradient} opacity-60 group-hover:opacity-100 transition-opacity duration-500`}></div>

              {/* Background glow on hover */}
              <div className={`absolute -top-20 -right-20 w-40 h-40 bg-gradient-to-br ${section.gradient} rounded-full blur-3xl opacity-0 group-hover:opacity-[0.07] transition-opacity duration-700`}></div>

              {/* Icon + Title */}
              <div className="relative z-10 flex items-center gap-3 sm:gap-4 mb-4 sm:mb-6">
                <div className={`w-9 h-9 xs:w-10 xs:h-10 sm:w-11 sm:h-11 md:w-12 md:h-12 rounded-lg sm:rounded-xl ${section.accentBg} flex items-center justify-center text-lg xs:text-xl sm:text-xl md:text-2xl shrink-0 group-hover:scale-110 transition-transform duration-300`}>
                  {section.icon}
                </div>
                <h3 className="text-base xs:text-lg sm:text-lg md:text-xl font-bold text-gray-900 dark:text-white tracking-tight leading-tight">{section.title}</h3>
              </div>

              {/* Divider */}
              <div className={`h-px w-full bg-gradient-to-r ${section.gradient} opacity-20 mb-4 sm:mb-6`}></div>

              {/* Items */}
              <ul className="relative z-10 space-y-2.5 sm:space-y-3 md:space-y-4">
                {section.items.map((item, i) => (
                  <motion.li
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 + i * 0.05 }}
                    className="flex items-start text-gray-600 dark:text-gray-300"
                  >
                    <span className={`${section.accentText} mr-3 mt-0.5 flex-shrink-0 font-bold`}>
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    </span>
                    <span className="leading-relaxed text-xs xs:text-[13px] sm:text-sm md:text-[15px]">{item}</span>
                  </motion.li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* CTA */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-4xl mx-auto mt-12 sm:mt-16 md:mt-20 text-center"
      >
        <div className="bg-gradient-to-r from-indigo-50/50 to-purple-50/50 dark:from-indigo-950/30 dark:to-purple-950/30 border border-indigo-500/20 rounded-xl sm:rounded-2xl p-5 xs:p-6 sm:p-8 md:p-10">
          <h2 className="text-xl xs:text-2xl sm:text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-3 sm:mb-4">Ready to Try It Out?</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-5 sm:mb-6 md:mb-8 text-sm sm:text-base md:text-lg">
            Experience the power of AI-driven fake news detection
          </p>
          <a
            href="/"
            className="inline-block px-6 py-3 sm:px-8 sm:py-3.5 md:px-10 md:py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold text-sm sm:text-base md:text-lg hover:shadow-lg hover:shadow-indigo-500/20 transition-all duration-300 hover:scale-105"
          >
            Start Verifying Now
          </a>
        </div>
      </motion.div>
      </div>
      <Footer />
    </div>
  );
};


export default HowItWorks;
