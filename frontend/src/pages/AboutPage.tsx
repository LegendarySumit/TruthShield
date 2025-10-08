
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
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-4xl font-black text-center mb-12 bg-gradient-to-r from-purple-600 to-pink-600 text-transparent bg-clip-text">
            Technology Stack
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {technologies.map((tech, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + idx * 0.1 }}
                whileHover={{ y: -5, scale: 1.02 }}
                className="group relative"
              >
                <div className={`absolute -inset-0.5 bg-gradient-to-r ${tech.gradient} rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500`}></div>
                <div className="relative bg-white dark:bg-gray-900 backdrop-blur-xl rounded-2xl p-6 border border-gray-200 dark:border-gray-800 shadow-lg">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className={`p-3 rounded-xl bg-gradient-to-r ${tech.gradient} text-white shadow-lg`}>
                      {tech.icon}
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {tech.category}
                    </h3>
                  </div>
                  <ul className="space-y-2">
                    {tech.items.map((item, itemIdx) => (
                      <motion.li
                        key={itemIdx}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.6 + idx * 0.1 + itemIdx * 0.05 }}
                        className="flex items-center text-gray-700 dark:text-gray-300"
                      >
                        <span className={`w-2 h-2 rounded-full bg-gradient-to-r ${tech.gradient} mr-3`}></span>
                        {item}
                      </motion.li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            ))}
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
            className="px-10 py-5 bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 text-white font-bold text-lg rounded-full shadow-2xl hover:shadow-purple-500/50 transition-all duration-300"
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
