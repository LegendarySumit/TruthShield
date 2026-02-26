
import { motion } from 'framer-motion';
import { SparklesIcon, CodeBracketIcon, CpuChipIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';
import Footer from '../components/Footer';

const AboutPage = () => {
  const technologies = [
    {
      category: 'Frontend',
      icon: <CodeBracketIcon className="h-8 w-8" />,
      items: ['React 19', 'TypeScript', 'Vite', 'TailwindCSS', 'Framer Motion'],
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      category: 'Backend',
      icon: <CpuChipIcon className="h-8 w-8" />,
      items: ['FastAPI', 'Python 3.13', 'Uvicorn', 'Pydantic'],
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      category: 'Machine Learning',
      icon: <SparklesIcon className="h-8 w-8" />,
      items: ['Scikit-learn', 'Pandas', 'TF-IDF Vectorization', 'Logistic Regression', 'NumPy'],
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      category: 'Deployment',
      icon: <ShieldCheckIcon className="h-8 w-8" />,
      items: ['Docker', 'Docker Compose', 'CORS', 'RESTful API'],
      gradient: 'from-orange-500 to-red-500'
    }
  ];

  return (
    <>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="max-w-6xl mx-auto py-24 px-4 sm:px-6 lg:px-8"
      >
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
            className="inline-block mb-6"
          >
            <div className="w-20 h-20 rounded-full bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 flex items-center justify-center shadow-2xl shadow-purple-500/50">
              <ShieldCheckIcon className="h-10 w-10 text-white" />
            </div>
          </motion.div>

          <h1 className="text-5xl md:text-6xl font-black bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 dark:from-purple-400 dark:via-pink-400 dark:to-red-400 text-transparent bg-clip-text mb-6">
            About TruthShield
          </h1>
          <p className="mt-4 max-w-3xl mx-auto text-xl text-gray-700 dark:text-gray-300 leading-relaxed">
            A cutting-edge <span className="font-bold text-purple-600 dark:text-purple-400">full-stack application</span> that leverages 
            <span className="font-bold text-pink-600 dark:text-pink-400"> artificial intelligence</span> to combat misinformation 
            and verify news authenticity in real-time.
          </p>
        </motion.div>

        {/* Mission Statement */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-16 relative"
        >
          <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl blur opacity-20"></div>
          <div className="relative bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl rounded-2xl p-8 border border-purple-200 dark:border-purple-800 shadow-xl">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
              <SparklesIcon className="h-8 w-8 mr-3 text-purple-600" />
              Our Mission
            </h2>
            <p className="text-lg text-gray-700 dark:text-gray-300 leading-relaxed">
              In an age where <span className="font-semibold text-red-600 dark:text-red-400">misinformation spreads faster than truth</span>, 
              TruthShield empowers individuals to make informed decisions. Our AI-powered platform analyzes news articles using advanced 
              machine learning algorithms, providing instant verification to help you distinguish fact from fiction.
            </p>
          </div>
        </motion.div>

        {/* Technologies Grid */}
        <div className="hidden">
           {/* Original content removed */}
        </div>

        {/* Contact Details */}
        <motion.div
           initial={{ opacity: 0, y: 30 }}
           animate={{ opacity: 1, y: 0 }}
           transition={{ delay: 0.4 }}
           className="mb-16"
        >
          <div className="relative overflow-hidden bg-gradient-to-br from-indigo-900 to-purple-900 rounded-3xl p-10 text-white shadow-2xl">
            {/* Background decorations */}
            <div className="absolute top-0 right-0 -mr-10 -mt-10 w-40 h-40 bg-pink-500 rounded-full blur-3xl opacity-20 animate-pulse"></div>
            <div className="absolute bottom-0 left-0 -ml-10 -mb-10 w-40 h-40 bg-blue-500 rounded-full blur-3xl opacity-20 animate-pulse"></div>

            <div className="relative z-10 text-center">
              <h2 className="text-3xl font-black mb-6 bg-gradient-to-r from-blue-200 to-pink-200 text-transparent bg-clip-text">
                Get in Touch
              </h2>
              <p className="text-blue-100 text-lg mb-8 max-w-2xl mx-auto">
                Have questions about our AI detection methodology or want to report a bug? We'd love to hear from you.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                <motion.div 
                  whileHover={{ y: -5 }}
                  className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 hover:bg-white/20 transition-all cursor-pointer"
                >
                  <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center mx-auto mb-4 text-blue-300">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                    </svg>
                  </div>
                  <h3 className="font-bold mb-2">Email Support</h3>
                  <p className="text-sm text-blue-100">contact@truthshield.ai</p>
                </motion.div>

                <motion.div 
                  whileHover={{ y: -5 }}
                  className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 hover:bg-white/20 transition-all cursor-pointer"
                >
                  <div className="w-12 h-12 bg-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-4 text-purple-300">
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
                    </svg>
                  </div>
                  <h3 className="font-bold mb-2">Media Inquiries</h3>
                  <p className="text-sm text-blue-100">press@truthshield.ai</p>
                </motion.div>

                <motion.div 
                  whileHover={{ y: -5 }}
                  className="bg-white/10 backdrop-blur-sm p-6 rounded-xl border border-white/20 hover:bg-white/20 transition-all cursor-pointer"
                >
                  <div className="w-12 h-12 bg-pink-500/20 rounded-full flex items-center justify-center mx-auto mb-4 text-pink-300">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                    </svg>
                  </div>
                  <h3 className="font-bold mb-2">Headquarters</h3>
                  <p className="text-sm text-blue-100">Silicon Valley, CA</p>
                </motion.div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-4xl font-black text-center mb-12 bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
            How It Works
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { step: '1', title: 'Submit Article', desc: 'Paste any news article text into our analyzer', icon: '📝' },
              { step: '2', title: 'AI Processing', desc: 'Our ML model analyzes patterns and linguistic features', icon: '🤖' },
              { step: '3', title: 'Get Results', desc: 'Receive instant verdict with confidence score', icon: '✅' }
            ].map((item, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.9 + idx * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="text-center"
              >
                <div className="text-6xl mb-4">{item.icon}</div>
                <div className="text-2xl font-black text-purple-600 dark:text-purple-400 mb-2">
                  Step {item.step}
                </div>
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                  {item.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {item.desc}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16"
        >
          {[
            { value: '99%', label: 'Accuracy Rate', gradient: 'from-green-500 to-emerald-500' },
            { value: '50K+', label: 'Active Users', gradient: 'from-blue-500 to-cyan-500' },
            { value: '1M+', label: 'Articles Verified', gradient: 'from-purple-500 to-pink-500' }
          ].map((stat, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.3 + idx * 0.1 }}
              whileHover={{ scale: 1.05 }}
              className="text-center p-8 rounded-2xl bg-gradient-to-br from-white to-gray-50 dark:from-gray-900 dark:to-gray-800 shadow-xl border border-gray-200 dark:border-gray-700"
            >
              <div className={`text-5xl font-black bg-gradient-to-r ${stat.gradient} text-transparent bg-clip-text mb-2`}>
                {stat.value}
              </div>
              <div className="text-gray-600 dark:text-gray-400 font-semibold">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.5 }}
          className="text-center"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.location.href = '/'}
            className="px-10 py-5 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 text-white font-bold text-lg rounded-full shadow-2xl hover:shadow-purple-500/20 transition-all duration-300"
          >
            Try TruthShield Now ✨
          </motion.button>
        </motion.div>
      </motion.div>
      
      <Footer />
    </>
  );
};

export default AboutPage;
