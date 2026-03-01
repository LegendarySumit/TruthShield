import { motion } from 'framer-motion';
import { DocumentTextIcon } from '@heroicons/react/24/outline';
import Footer from '../components/Footer';

const sections = [
  {
    title: 'Acceptance of Terms',
    content:
      'By accessing or using TruthShield ("the Service"), you agree to be bound by these Terms of Service. If you do not agree, please discontinue use of the Service immediately.',
  },
  {
    title: 'Description of Service',
    content:
      'TruthShield is an AI-powered tool that analyzes submitted text and returns a non-binding prediction of whether the content exhibits patterns associated with misinformation. Results are provided for informational and research purposes only.',
  },
  {
    title: 'No Guarantee of Accuracy',
    content:
      'Our predictions are probabilistic and may be incorrect. TruthShield is a supplementary research aid, not a replacement for professional journalism, legal advice, or independent fact-checking. We make no warranty — express or implied — regarding the accuracy or completeness of any result.',
  },
  {
    title: 'Acceptable Use',
    content:
      'You agree not to: (a) submit content that is harmful, defamatory, or illegal; (b) attempt to reverse-engineer, overload, or exploit the Service; (c) use automated bots or scrapers against the API without prior written consent; or (d) misrepresent TruthShield\'s output as definitive legal or scientific fact.',
  },
  {
    title: 'Intellectual Property',
    content:
      'All code, models, branding, and UI elements of TruthShield are owned by or licensed to TruthShield. The underlying open-source libraries retain their respective licenses. You may not reproduce or redistribute TruthShield\'s proprietary components without permission.',
  },
  {
    title: 'Limitation of Liability',
    content:
      'To the maximum extent permitted by law, TruthShield and its contributors shall not be liable for any indirect, incidental, or consequential damages arising from your use of or reliance on the Service, including but not limited to decisions made based on prediction results.',
  },
  {
    title: 'Third-Party Links & APIs',
    content:
      'The Service may interact with third-party APIs (e.g. Google Gemini). TruthShield is not responsible for the availability, accuracy, or policies of those services. Use of third-party services is governed by their respective terms.',
  },
  {
    title: 'Modifications',
    content:
      'We reserve the right to modify these terms at any time. Continued use of the Service after a revision constitutes acceptance. We will update the "Last revised" date whenever changes are made.',
  },
  {
    title: 'Governing Law',
    content:
      'These Terms shall be governed by and construed in accordance with the laws of the State of California, United States, without regard to conflict-of-law principles.',
  },
  {
    title: 'Contact',
    content:
      'Questions about these terms? Email us at contact@truthshield.ai. We aim to respond within 2 business days.',
  },
];

const TermsPage = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-1 pt-16 sm:pt-18 md:pt-20 pb-10 sm:pb-12 md:pb-16 px-3 xs:px-4">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-3xl mx-auto text-center mb-8 sm:mb-12"
        >
          <div className="w-14 h-14 xs:w-16 xs:h-16 sm:w-18 sm:h-18 md:w-20 md:h-20 mx-auto mb-4 sm:mb-6 rounded-full bg-gradient-to-r from-violet-500 to-purple-500 flex items-center justify-center">
            <DocumentTextIcon className="w-8 h-8 xs:w-9 xs:h-9 sm:w-10 sm:h-10 md:w-12 md:h-12 text-white" />
          </div>
          <h1 className="text-2xl xs:text-3xl sm:text-4xl md:text-5xl font-bold mb-3 sm:mb-4 bg-gradient-to-r from-violet-400 via-purple-500 to-indigo-500 text-transparent bg-clip-text">
            Terms of Service
          </h1>
          <p className="text-sm sm:text-base text-gray-500 dark:text-gray-400">
            Last revised: <span className="font-semibold text-violet-500">March 2026</span>
          </p>
          <p className="mt-3 text-base sm:text-lg text-gray-600 dark:text-gray-300 max-w-xl mx-auto">
            Please read these terms carefully before using TruthShield.
          </p>
        </motion.div>

        {/* Sections */}
        <div className="max-w-3xl mx-auto space-y-3 sm:space-y-4">
          {sections.map((section, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.04 }}
              className="bg-white/80 dark:bg-gray-950/50 backdrop-blur-xl border border-violet-500/20 rounded-2xl p-4 xs:p-5 sm:p-6 hover:border-violet-500/40 transition-all duration-300"
            >
              <h2 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-white mb-2">
                <span className="text-violet-500 mr-2">{String(index + 1).padStart(2, '0')}.</span>
                {section.title}
              </h2>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                {section.content}
              </p>
            </motion.div>
          ))}
        </div>

      </div>
      <Footer />
    </div>
  );
};

export default TermsPage;
