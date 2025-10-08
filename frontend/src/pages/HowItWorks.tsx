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
      color: 'from-purple-400 to-pink-500'
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
      color: 'from-orange-400 to-red-500'
    },
    {
      icon: ShieldCheckIcon,
      title: '5. Confidence Calculation',
      description: 'The model generates a probability score (0-100%) indicating confidence in its prediction. Higher scores mean stronger certainty.',
      color: 'from-pink-400 to-rose-500'
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
      items: [
        'Tokenization and lemmatization',
        'Stop word removal (English)',
        'N-gram analysis (unigrams + bigrams)',
        'TF-IDF vectorization with 5000 max features'
      ]
    },
    {
      title: 'Machine Learning Model',
      items: [
        'Algorithm: Logistic Regression',
        'Training samples: 640 balanced articles',
        'Test accuracy: 100% on 160 samples',
        'Regularization: L2 with balanced class weights'
      ]
    },
    {
      title: 'Fake News Indicators',
      items: [
        'Sensational language & clickbait',
        'Emotional manipulation patterns',
        'Lack of credible source attribution',
        'Unusual punctuation and capitalization'
      ]
    }
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
          How It Works
        </h1>
        <p className="text-xl text-gray-400">
          Discover the science behind fake news detection
        </p>
      </motion.div>

      {/* Process Steps */}
      <div className="max-w-6xl mx-auto mb-20">
        {steps.map((step, index) => (
          <motion.div
            key={step.title}
            initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: index * 0.1 }}
            className="relative mb-12 last:mb-0"
          >
            <div className="flex items-start gap-6">
              {/* Icon */}
              <div className="flex-shrink-0">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${step.color} p-3 shadow-lg`}>
                  <step.icon className="w-full h-full text-white" />
                </div>
              </div>

              {/* Content */}
              <div className="flex-1 bg-gray-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 hover:border-purple-500/50 transition-all duration-300">
                <h3 className="text-2xl font-bold text-white mb-3">{step.title}</h3>
                <p className="text-gray-300 leading-relaxed">{step.description}</p>
              </div>
            </div>

            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className="absolute left-8 top-20 w-0.5 h-12 bg-gradient-to-b from-purple-500/50 to-transparent" />
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
        <h2 className="text-4xl font-bold text-center mb-12 text-white">
          Technical Deep Dive
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {technicalDetails.map((section, index) => (
            <motion.div
              key={section.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="bg-gray-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6 hover:border-purple-500/50 transition-all duration-300"
            >
              <h3 className="text-xl font-bold text-white mb-4">{section.title}</h3>
              <ul className="space-y-3">
                {section.items.map((item, i) => (
                  <li key={i} className="flex items-start text-gray-300">
                    <span className="text-purple-400 mr-2 mt-1">✓</span>
                    <span>{item}</span>
                  </li>
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
        className="max-w-4xl mx-auto mt-20 text-center"
      >
        <div className="bg-gradient-to-r from-purple-900/20 to-pink-900/20 border border-purple-500/20 rounded-2xl p-10">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Try It Out?</h2>
          <p className="text-gray-400 mb-8 text-lg">
            Experience the power of AI-driven fake news detection
          </p>
          <a
            href="/"
            className="inline-block px-10 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold text-lg hover:shadow-lg hover:shadow-purple-500/50 transition-all duration-300 hover:scale-105"
          >
            Start Verifying Now
          </a>
        </div>
      </motion.div>
    </div>
  );
};

export default HowItWorks;
