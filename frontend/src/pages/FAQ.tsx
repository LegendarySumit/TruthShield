import React from 'react';
import { motion } from 'framer-motion';
import { QuestionMarkCircleIcon } from '@heroicons/react/24/outline';

const FAQ: React.FC = () => {
  const faqs = [
    {
      question: 'How accurate is TruthShield?',
      answer: 'TruthShield achieves 100% accuracy on our test dataset of 160 articles. The model is trained on 800 balanced samples using advanced NLP techniques including TF-IDF vectorization and Logistic Regression.'
    },
    {
      question: 'What makes news "fake"?',
      answer: 'Fake news typically contains sensational language, unverified claims, misleading headlines, lack of credible sources, emotional manipulation, and false statistics. Our model identifies these patterns through machine learning.'
    },
    {
      question: 'How does the detection work?',
      answer: 'We use Natural Language Processing (NLP) with TF-IDF (Term Frequency-Inverse Document Frequency) to analyze text patterns. The model extracts 1,360 features and uses Logistic Regression to classify news as real or fake with confidence scores.'
    },
    {
      question: 'Can I trust the confidence score?',
      answer: 'Yes! Confidence scores between 70-80% indicate strong predictions. Scores above 80% show very high confidence. The model considers linguistic patterns, word usage, and statistical features to calculate accuracy.'
    },
    {
      question: 'What happens if I submit short text?',
      answer: 'You need at least 50 characters for accurate analysis. Short texts don\'t provide enough context for the model to make reliable predictions. We recommend submitting the full headline and lead paragraph.'
    },
    {
      question: 'Is my data stored or shared?',
      answer: 'No. All analysis happens in real-time and your text is never stored in our database. We respect your privacy and don\'t track, store, or share any submitted content.'
    },
    {
      question: 'Can it detect satire?',
      answer: 'Satire can be challenging as it often mimics fake news intentionally. Our model is trained on factual news vs. fake news, not satire. Satirical content may be flagged as fake depending on language patterns.'
    },
    {
      question: 'How often is the model updated?',
      answer: 'We continuously improve our model with new training data and enhanced algorithms. Current version was trained with advanced preprocessing including bigram analysis and balanced class weights.'
    },
    {
      question: 'What if the prediction seems wrong?',
      answer: 'No model is perfect. If you believe a prediction is incorrect, consider: 1) The source credibility, 2) Fact-check with multiple sources, 3) Look for evidence and citations. Always use critical thinking alongside AI.'
    },
    {
      question: 'Can I use TruthShield for research?',
      answer: 'Yes! TruthShield is built with open-source technologies. The model uses scikit-learn and can be used for educational research. Contact us for API access or bulk analysis capabilities.'
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
        <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
          <QuestionMarkCircleIcon className="w-12 h-12 text-white" />
        </div>
        <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 text-transparent bg-clip-text">
          Frequently Asked Questions
        </h1>
        <p className="text-xl text-gray-400">
          Everything you need to know about TruthShield
        </p>
      </motion.div>

      {/* FAQ List */}
      <div className="max-w-4xl mx-auto space-y-4">
        {faqs.map((faq, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
            className="bg-white/80 dark:bg-gray-900/50 backdrop-blur-xl border border-purple-500/20 rounded-2xl overflow-hidden hover:border-purple-500/50 transition-all duration-300"
          >
            <details className="group">
              <summary className="flex items-center justify-between cursor-pointer p-6 hover:bg-gray-100/50 dark:hover:bg-gray-800/50 transition-colors">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white pr-4">{faq.question}</h3>
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center group-open:rotate-180 transition-transform">
                  <svg className="w-4 h-4 text-purple-500 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </summary>
              <div className="px-6 pb-6 text-gray-700 dark:text-gray-300 leading-relaxed border-t border-gray-300/50 dark:border-gray-800/50 pt-4">
                {faq.answer}
              </div>
            </details>
          </motion.div>
        ))}
      </div>

      {/* Still Have Questions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="max-w-4xl mx-auto mt-16 text-center"
      >
        <div className="bg-gradient-to-r from-purple-100/50 to-pink-100/50 dark:from-purple-900/20 dark:to-pink-900/20 border border-purple-500/20 rounded-2xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Still have questions?</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Can't find the answer you're looking for? We're here to help!
          </p>
          <a 
            href="mailto:support@truthshield.ai?subject=Support Request&body=Hello TruthShield Team,%0D%0A%0D%0AI have a question about..."
            className="inline-block px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all duration-300 hover:scale-105"
          >
            Contact Support
          </a>
        </div>
      </motion.div>
    </div>
  );
};

export default FAQ;
