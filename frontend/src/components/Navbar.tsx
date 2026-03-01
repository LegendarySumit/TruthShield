
import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { SunIcon, MoonIcon, ShieldCheckIcon, Bars3Icon, XMarkIcon } from '@heroicons/react/24/solid';
import { motion, AnimatePresence } from 'framer-motion';

const Navbar = () => {
  // Read saved preference; fall back to dark if nothing is stored
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('theme') !== 'light');
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, type: 'spring' }}
      className={`fixed w-full z-50 top-0 transition-all duration-300 border-b ${
        scrolled 
          ? 'bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl shadow-lg shadow-purple-500/10 border-gray-200/60 dark:border-indigo-500/15' 
          : 'bg-white/60 dark:bg-gray-900/60 backdrop-blur-lg border-gray-200/30 dark:border-gray-700/30'
      }`}
    >
      <div className="max-w-7xl mx-auto px-3 xs:px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16 md:h-20">
          {/* Logo with Gradient */}
          <motion.div 
            className="flex items-center space-x-2 sm:space-x-3 flex-shrink min-w-0"
            whileHover={{ scale: 1.05 }}
            transition={{ type: 'spring', stiffness: 400 }}
          >
            <NavLink to="/" className="flex items-center space-x-2 sm:space-x-3 group min-w-0">
              <motion.div
                animate={{ rotate: [0, 5, -5, 0] }}
                transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
                className="relative flex-shrink-0"
              >
                <ShieldCheckIcon className="h-8 w-8 sm:h-10 sm:w-10 text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 via-purple-500 to-violet-500" />
                <motion.div
                  className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-violet-500 rounded-lg blur-xl opacity-30"
                  animate={{ opacity: [0.3, 0.6, 0.3] }}
                  transition={{ duration: 2, repeat: Infinity }}
                />
              </motion.div>
              <div className="flex flex-col min-w-0">
                <span className="text-lg sm:text-2xl font-black bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 dark:from-indigo-400 dark:via-purple-400 dark:to-violet-400 text-transparent bg-clip-text whitespace-nowrap">
                  TruthShield
                </span>
                <span className="text-[10px] sm:text-xs font-medium text-gray-500 dark:text-gray-400 -mt-1 hidden xs:block">
                  AI-Powered Verification
                </span>
              </div>
            </NavLink>
          </motion.div>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-2">
            <NavLink to="/">
              {({ isActive }) => (
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-5 py-2.5 rounded-full font-semibold transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  Home
                </motion.div>
              )}
            </NavLink>
            
            <NavLink to="/how-it-works">
              {({ isActive }) => (
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-5 py-2.5 rounded-full font-semibold transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  How It Works
                </motion.div>
              )}
            </NavLink>
            
            <NavLink to="/statistics">
              {({ isActive }) => (
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-5 py-2.5 rounded-full font-semibold transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  Statistics
                </motion.div>
              )}
            </NavLink>
            
            <NavLink to="/faq">
              {({ isActive }) => (
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-5 py-2.5 rounded-full font-semibold transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  FAQ
                </motion.div>
              )}
            </NavLink>
            
            <NavLink to="/about">
              {({ isActive }) => (
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className={`px-5 py-2.5 rounded-full font-semibold transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                  }`}
                >
                  About
                </motion.div>
              )}
            </NavLink>

            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.1, rotate: 180 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setDarkMode(!darkMode)}
              className="p-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10 hover:shadow-lg transition-all duration-300 ml-2"
            >
              {darkMode ? (
                <SunIcon className="h-5 w-5" />
              ) : (
                <MoonIcon className="h-5 w-5" />
              )}
            </motion.button>
          </div>

          {/* Mobile Navigation */}
          <div className="flex md:hidden items-center space-x-2 xs:space-x-2.5 sm:space-x-3 flex-shrink-0">
            {/* Theme Toggle */}
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 sm:p-2.5 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-md shadow-indigo-500/10"
            >
              {darkMode ? (
                <SunIcon className="h-4 w-4 sm:h-5 sm:w-5" />
              ) : (
                <MoonIcon className="h-4 w-4 sm:h-5 sm:w-5" />
              )}
            </motion.button>

            {/* Hamburger Menu */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 sm:p-2.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300"
            >
              {mobileMenuOpen ? (
                <XMarkIcon className="h-5 w-5 sm:h-6 sm:w-6" />
              ) : (
                <Bars3Icon className="h-5 w-5 sm:h-6 sm:w-6" />
              )}
            </motion.button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="md:hidden bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl border-t border-purple-500/20"
          >
            <div className="px-3 py-3 space-y-1.5 sm:px-4 sm:py-4 sm:space-y-2">
              <NavLink 
                to="/" 
                onClick={() => setMobileMenuOpen(false)}
              >
                {({ isActive }) => (
                  <motion.div
                    whileTap={{ scale: 0.98 }}
                    className={`block px-3 py-2.5 sm:px-4 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    Home
                  </motion.div>
                )}
              </NavLink>
              
              <NavLink 
                to="/how-it-works" 
                onClick={() => setMobileMenuOpen(false)}
              >
                {({ isActive }) => (
                  <motion.div
                    whileTap={{ scale: 0.98 }}
                    className={`block px-3 py-2.5 sm:px-4 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    How It Works
                  </motion.div>
                )}
              </NavLink>
              
              <NavLink 
                to="/statistics" 
                onClick={() => setMobileMenuOpen(false)}
              >
                {({ isActive }) => (
                  <motion.div
                    whileTap={{ scale: 0.98 }}
                    className={`block px-3 py-2.5 sm:px-4 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    Statistics
                  </motion.div>
                )}
              </NavLink>
              
              <NavLink 
                to="/faq" 
                onClick={() => setMobileMenuOpen(false)}
              >
                {({ isActive }) => (
                  <motion.div
                    whileTap={{ scale: 0.98 }}
                    className={`block px-3 py-2.5 sm:px-4 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    FAQ
                  </motion.div>
                )}
              </NavLink>
              
              <NavLink 
                to="/about" 
                onClick={() => setMobileMenuOpen(false)}
              >
                {({ isActive }) => (
                  <motion.div
                    whileTap={{ scale: 0.98 }}
                    className={`block px-3 py-2.5 sm:px-4 sm:py-3 rounded-lg font-semibold text-sm sm:text-base transition-all duration-300 ${
                      isActive
                        ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white shadow-lg'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    About
                  </motion.div>
                )}
              </NavLink>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};

export default Navbar;
