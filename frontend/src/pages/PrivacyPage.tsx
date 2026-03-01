import { motion } from 'framer-motion';
import { ShieldCheckIcon } from '@heroicons/react/24/outline';
import Footer from '../components/Footer';

const sections = [
  {
    title: 'Information We Collect',
    content:
      'TruthShield does not require you to create an account or provide personal details to use the service. The only data we process is the text you voluntarily submit for analysis. This text is passed to our AI engine in real-time and is never written to a database or log file.',
  },
  {
    title: 'How We Use Your Data',
    content:
      'Submitted text is used solely to generate a fake-news prediction and confidence score. It is not used for advertising, sold to third parties, or retained after the request completes. Aggregate, anonymised metrics (e.g. total requests per day) may be collected to monitor service health.',
  },
  {
    title: 'Third-Party Services',
    content:
      'Results may be enhanced by the Google Gemini API. Text sent to Gemini is subject to Google\'s own privacy policy (policies.google.com). No other third-party analytics or tracking scripts are embedded in TruthShield.',
  },
  {
    title: 'Cookies & Local Storage',
    content:
      'We store a single key ("theme") in your browser\'s localStorage to remember your light/dark mode preference. No tracking cookies, session identifiers, or fingerprinting techniques are used.',
  },
  {
    title: 'Data Security',
    content:
      'All communication between your browser and our servers is encrypted via HTTPS/TLS. Because we do not persist submitted text, there is no user data at risk of a database breach.',
  },
  {
    title: 'Children\'s Privacy',
    content:
      'TruthShield is a general-purpose research tool and is not directed at children under 13. We do not knowingly collect information from minors.',
  },
  {
    title: 'Changes to This Policy',
    content:
      'We may update this policy as the product evolves. Material changes will be reflected with an updated "Last revised" date at the top of this page. Continued use of TruthShield after changes constitutes acceptance of the revised policy.',
  },
  {
    title: 'Contact',
    content:
      'Questions about this privacy policy? Reach us at contact@truthshield.ai and we\'ll respond within 2 business days.',
  },
];

const PrivacyPage = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-1 pt-16 sm:pt-18 md:pt-20 pb-10 sm:pb-12 md:pb-16 px-3 xs:px-4">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-3xl mx-auto text-center mb-8 sm:mb-12"
        >
          <div className="w-14 h-14 xs:w-16 xs:h-16 sm:w-18 sm:h-18 md:w-20 md:h-20 mx-auto mb-4 sm:mb-6 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center">
            <ShieldCheckIcon className="w-8 h-8 xs:w-9 xs:h-9 sm:w-10 sm:h-10 md:w-12 md:h-12 text-white" />
          </div>
          <h1 className="text-2xl xs:text-3xl sm:text-4xl md:text-5xl font-bold mb-3 sm:mb-4 bg-gradient-to-r from-indigo-400 via-purple-500 to-violet-500 text-transparent bg-clip-text">
            Privacy Policy
          </h1>
          <p className="text-sm sm:text-base text-gray-500 dark:text-gray-400">
            Last revised: <span className="font-semibold text-indigo-500">March 2026</span>
          </p>
          <p className="mt-3 text-base sm:text-lg text-gray-600 dark:text-gray-300 max-w-xl mx-auto">
            We built TruthShield with privacy first. Here's everything we do — and don't do — with your data.
          </p>
        </motion.div>

        {/* Sections */}
        <div className="max-w-3xl mx-auto space-y-3 sm:space-y-4">
          {sections.map((section, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="bg-white/80 dark:bg-gray-950/50 backdrop-blur-xl border border-indigo-500/20 rounded-2xl p-4 xs:p-5 sm:p-6 hover:border-indigo-500/40 transition-all duration-300"
            >
              <h2 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-white mb-2">
                <span className="text-indigo-500 mr-2">{String(index + 1).padStart(2, '0')}.</span>
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

export default PrivacyPage;
