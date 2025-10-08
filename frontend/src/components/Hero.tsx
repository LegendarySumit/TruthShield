
import { motion } from 'framer-motion';
import { SparklesIcon, ShieldCheckIcon, BoltIcon } from '@heroicons/react/24/solid';

const Hero = () => {
  return (
    <div className="relative text-center py-24 px-4 sm:px-6 lg:px-8 overflow-hidden">
      {/* Floating particles */}
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-2 h-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"
          animate={{
            x: [Math.random() * 100 - 50, Math.random() * 100 - 50],
            y: [Math.random() * 100 - 50, Math.random() * 100 - 50],
            opacity: [0.2, 0.8, 0.2],
            scale: [1, 1.5, 1],
          }}
          transition={{
            duration: 3 + Math.random() * 2,
            repeat: Infinity,
            delay: i * 0.3,
          }}
          style={{
            left: `${20 + i * 15}%`,
            top: `${30 + (i % 3) * 20}%`,
          }}
        />
      ))}

      {/* Main Title with Gradient */}
      <motion.div
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, type: 'spring', stiffness: 100 }}
        className="relative"
      >
        <motion.div
          animate={{ 
            backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
          }}
          transition={{ duration: 5, repeat: Infinity, ease: 'linear' }}
          className="inline-block"
        >
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-black bg-gradient-to-r from-purple-600 via-pink-600 to-red-600 dark:from-purple-400 dark:via-pink-400 dark:to-red-400 text-transparent bg-clip-text mb-4 bg-[length:200%_100%]">
            Unmask the Truth
          </h1>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex items-center justify-center space-x-2 mb-6"
        >
          <SparklesIcon className="h-6 w-6 text-yellow-500" />
          <h2 className="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-yellow-500">
            AI-Powered News Verification
          </h2>
          <SparklesIcon className="h-6 w-6 text-yellow-500" />
        </motion.div>
      </motion.div>

      {/* Subtitle */}
      <motion.p
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="mt-6 max-w-3xl mx-auto text-lg md:text-xl text-gray-700 dark:text-gray-300 leading-relaxed"
      >
        In an era of <span className="font-bold text-purple-600 dark:text-purple-400">misinformation</span> and <span className="font-bold text-pink-600 dark:text-pink-400">fake news</span>, 
        our cutting-edge AI technology helps you distinguish <span className="font-bold text-green-600 dark:text-green-400">fact from fiction</span>. 
        Get instant, accurate analysis of any news article.
      </motion.p>

      {/* Feature Pills */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.7 }}
        className="mt-10 flex flex-wrap items-center justify-center gap-4"
      >
        <motion.div
          whileHover={{ scale: 1.05, y: -5 }}
          className="flex items-center space-x-2 px-6 py-3 rounded-full bg-gradient-to-r from-purple-500/20 to-pink-500/20 dark:from-purple-500/30 dark:to-pink-500/30 backdrop-blur-sm border border-purple-300 dark:border-purple-500"
        >
          <ShieldCheckIcon className="h-5 w-5 text-purple-600 dark:text-purple-400" />
          <span className="font-semibold text-gray-800 dark:text-gray-200">99% Accuracy</span>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.05, y: -5 }}
          className="flex items-center space-x-2 px-6 py-3 rounded-full bg-gradient-to-r from-blue-500/20 to-cyan-500/20 dark:from-blue-500/30 dark:to-cyan-500/30 backdrop-blur-sm border border-blue-300 dark:border-blue-500"
        >
          <BoltIcon className="h-5 w-5 text-blue-600 dark:text-blue-400" />
          <span className="font-semibold text-gray-800 dark:text-gray-200">Instant Analysis</span>
        </motion.div>

        <motion.div
          whileHover={{ scale: 1.05, y: -5 }}
          className="flex items-center space-x-2 px-6 py-3 rounded-full bg-gradient-to-r from-green-500/20 to-emerald-500/20 dark:from-green-500/30 dark:to-emerald-500/30 backdrop-blur-sm border border-green-300 dark:border-green-500"
        >
          <SparklesIcon className="h-5 w-5 text-green-600 dark:text-green-400" />
          <span className="font-semibold text-gray-800 dark:text-gray-200">Free to Use</span>
        </motion.div>
      </motion.div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1, y: [0, 10, 0] }}
        transition={{ opacity: { delay: 1.5 }, y: { duration: 1.5, repeat: Infinity } }}
        className="mt-16"
      >
        <div className="w-6 h-10 border-2 border-purple-500 rounded-full mx-auto relative">
          <motion.div
            animate={{ y: [0, 16, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="w-1.5 h-1.5 bg-purple-500 rounded-full absolute left-1/2 transform -translate-x-1/2 top-2"
          />
        </div>
      </motion.div>
    </div>
  );
};

export default Hero;
