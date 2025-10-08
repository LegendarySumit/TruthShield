
import { motion } from 'framer-motion';
import { HeartIcon, ShieldCheckIcon } from '@heroicons/react/24/solid';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative mt-20 bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 opacity-10">
        <motion.div
          className="absolute top-0 left-0 w-64 h-64 bg-purple-500 rounded-full blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, 50, 0],
          }}
          transition={{ duration: 20, repeat: Infinity }}
        />
        <motion.div
          className="absolute bottom-0 right-0 w-64 h-64 bg-pink-500 rounded-full blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, -50, 0],
          }}
          transition={{ duration: 25, repeat: Infinity }}
        />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="flex items-center space-x-3 mb-4"
            >
              <ShieldCheckIcon className="h-10 w-10 text-purple-400" />
              <div>
                <h3 className="text-2xl font-black bg-gradient-to-r from-purple-400 via-pink-400 to-red-400 text-transparent bg-clip-text">
                  TruthShield
                </h3>
                <p className="text-xs text-gray-400">AI-Powered Verification</p>
              </div>
            </motion.div>
            <p className="text-gray-300 text-sm leading-relaxed mb-4">
              Empowering truth in the digital age. Our advanced AI technology helps millions 
              distinguish fact from fiction, making the internet a safer place for everyone.
            </p>
            <div className="flex items-center space-x-2 text-sm text-purple-300">
              <ShieldCheckIcon className="h-4 w-4" />
              <span>99% Accuracy • 50K+ Active Users • 1M+ Articles Verified</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-400 text-transparent bg-clip-text">
              Quick Links
            </h4>
            <ul className="space-y-2">
              {['Home', 'About', 'How It Works', 'API', 'Blog'].map((link, idx) => (
                <motion.li
                  key={idx}
                  whileHover={{ x: 5 }}
                  className="text-gray-300 hover:text-purple-400 transition-colors cursor-pointer text-sm"
                >
                  {link}
                </motion.li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-lg font-bold mb-4 bg-gradient-to-r from-pink-400 to-red-400 text-transparent bg-clip-text">
              Resources
            </h4>
            <ul className="space-y-2">
              {['Documentation', 'Support', 'Privacy Policy', 'Terms of Service', 'Contact'].map((link, idx) => (
                <motion.li
                  key={idx}
                  whileHover={{ x: 5 }}
                  className="text-gray-300 hover:text-pink-400 transition-colors cursor-pointer text-sm"
                >
                  {link}
                </motion.li>
              ))}
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-700 mb-8"></div>

        {/* Bottom Section */}
        <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
          <motion.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-sm text-gray-400 flex items-center"
          >
            © {currentYear} TruthShield. Made with
            <motion.span
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
              className="mx-1"
            >
              <HeartIcon className="h-4 w-4 text-red-500 inline" />
            </motion.span>
            for a better internet
          </motion.p>

          {/* Social Links */}
          <div className="flex items-center space-x-4">
            {['Twitter', 'GitHub', 'LinkedIn', 'Discord'].map((social, idx) => (
              <motion.button
                key={idx}
                whileHover={{ scale: 1.1, y: -2 }}
                whileTap={{ scale: 0.95 }}
                className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-600 to-pink-600 flex items-center justify-center text-white font-bold text-xs shadow-lg hover:shadow-purple-500/50 transition-all"
              >
                {social[0]}
              </motion.button>
            ))}
          </div>
        </div>

        {/* Tech Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-8 text-center"
        >
          <p className="text-xs text-gray-500">
            Powered by Advanced AI • Built with React, TypeScript & FastAPI
          </p>
        </motion.div>
      </div>
    </footer>
  );
};

export default Footer;
