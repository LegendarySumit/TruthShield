
import { motion } from 'framer-motion';
import { StarIcon, UserCircleIcon } from '@heroicons/react/24/solid';

const testimonials = [
  {
    quote: "This tool is an absolute game-changer for my research. I can quickly verify sources and avoid spreading misinformation. The AI is incredibly accurate!",
    name: "Dr. Evelyn Reed",
    title: "University Professor",
    role: "Academic Research",
    rating: 5,
    image: "👩‍🏫",
    gradient: "from-blue-500 to-cyan-500"
  },
  {
    quote: "As an investigative journalist, I rely on this every single day. The accuracy is mind-blowing, and it saves me countless hours of fact-checking. Highly recommended!",
    name: "Marcus Chen",
    title: "Investigative Journalist",
    role: "News Media",
    rating: 5,
    image: "👨‍💼",
    gradient: "from-indigo-500 to-purple-500"
  },
  {
    quote: "Finally, a simple and effective way to check the news my family shares on social media. This has become absolutely essential in my daily life!",
    name: "Sarah Williams",
    title: "Digital Content Creator",
    role: "Social Media",
    rating: 5,
    image: "👩‍💻",
    gradient: "from-purple-500 to-violet-500"
  },
];

const Reviews = () => {
  return (
    <div className="py-10 sm:py-14 md:py-20 relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-indigo-50/30 to-transparent dark:via-indigo-950/10" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8 sm:mb-12 md:mb-16"
        >
          <motion.div
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: 'spring', stiffness: 200 }}
            className="inline-flex items-center space-x-2 mb-4"
          >
            {[...Array(5)].map((_, i) => (
              <StarIcon key={i} className="h-5 w-5 xs:h-6 xs:w-6 sm:h-7 sm:w-7 md:h-8 md:w-8 text-yellow-400" />
            ))}
          </motion.div>
          
          <h2 className="text-2xl xs:text-3xl sm:text-4xl md:text-5xl font-black bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 dark:from-indigo-400 dark:via-purple-400 dark:to-violet-400 text-transparent bg-clip-text mb-3 sm:mb-4">
            Loved by Thousands
          </h2>
          
          <p className="mt-3 sm:mt-4 max-w-2xl mx-auto text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-300">
            From researchers to everyday readers, professionals trust our AI-powered verification
          </p>

          {/* Stats */}
          <div className="mt-6 sm:mt-8 flex flex-wrap justify-center gap-4 xs:gap-5 sm:gap-6 md:gap-8">
            {[
              { value: '50K+', label: 'Active Users' },
              { value: '1M+', label: 'Articles Verified' },
              { value: '99%', label: 'Accuracy Rate' }
            ].map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.5 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1, type: 'spring' }}
                className="text-center"
              >
                <div className="text-xl xs:text-2xl sm:text-3xl font-black bg-gradient-to-r from-indigo-600 to-purple-600 text-transparent bg-clip-text">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 font-medium">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="group relative"
            >
              {/* Glowing effect */}
              <div className={`absolute -inset-0.5 bg-gradient-to-r ${testimonial.gradient} rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500`} />
              
              <div className="relative bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl p-4 xs:p-5 sm:p-6 md:p-8 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-800 hover:shadow-2xl transition-all duration-300">
                {/* Rating Stars */}
                <div className="flex items-center space-x-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, scale: 0 }}
                      whileInView={{ opacity: 1, scale: 1 }}
                      viewport={{ once: true }}
                      transition={{ delay: 0.5 + (i * 0.1) }}
                    >
                      <StarIcon className="h-5 w-5 text-yellow-400" />
                    </motion.div>
                  ))}
                </div>

                {/* Quote */}
                <p className="text-sm sm:text-base text-gray-700 dark:text-gray-300 leading-relaxed mb-4 sm:mb-6 italic">
                  "{testimonial.quote}"
                </p>

                {/* User Info */}
                <div className="flex items-center space-x-3 sm:space-x-4 pt-3 sm:pt-4 border-t border-gray-200 dark:border-gray-700">
                  <motion.div
                    whileHover={{ rotate: 360, scale: 1.1 }}
                    transition={{ duration: 0.5 }}
                    className={`w-10 h-10 xs:w-11 xs:h-11 sm:w-12 sm:h-12 md:w-14 md:h-14 rounded-full bg-gradient-to-r ${testimonial.gradient} flex items-center justify-center text-xl xs:text-2xl sm:text-2xl md:text-3xl shadow-lg`}
                  >
                    {testimonial.image}
                  </motion.div>
                  
                  <div>
                    <p className="font-bold text-gray-900 dark:text-white">
                      {testimonial.name}
                    </p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {testimonial.title}
                    </p>
                    <p className={`text-xs font-semibold bg-gradient-to-r ${testimonial.gradient} text-transparent bg-clip-text`}>
                      {testimonial.role}
                    </p>
                  </div>
                </div>

                {/* Verified badge */}
                <motion.div
                  initial={{ opacity: 0, scale: 0 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.8 }}
                  className="absolute top-4 right-4"
                >
                  <div className={`px-3 py-1 rounded-full bg-gradient-to-r ${testimonial.gradient} text-white text-xs font-bold shadow-lg flex items-center space-x-1`}>
                    <UserCircleIcon className="h-3 w-3" />
                    <span>Verified</span>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
          className="text-center mt-10 sm:mt-12 md:mt-16"
        >
          <p className="text-gray-600 dark:text-gray-400 text-sm sm:text-base md:text-lg mb-3 sm:mb-4">
            Join thousands of satisfied users today!
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
            className="px-5 py-3 xs:px-6 sm:px-8 sm:py-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-violet-600 text-white font-bold text-sm sm:text-base rounded-full shadow-xl hover:shadow-2xl hover:shadow-indigo-500/20 transition-all duration-300"
          >
            Try It Now - It's Free! ✨
          </motion.button>
        </motion.div>
      </div>
    </div>
  );
};

export default Reviews;
