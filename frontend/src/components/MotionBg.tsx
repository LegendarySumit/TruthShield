
import { motion } from 'framer-motion';

// Stable particle data computed once at module load — avoids re-randomising on every render
const PARTICLES = Array.from({ length: 15 }, (_, i) => ({
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  animateX: Math.random() * 20 - 10,
  duration: 3 + Math.random() * 3,
  delay: Math.random() * 2,
  colorClass: i % 3 === 0 ? 'bg-indigo-400' : i % 3 === 1 ? 'bg-purple-400' : 'bg-violet-400',
}));

const MotionBg = () => {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden bg-gradient-to-br from-gray-50 via-indigo-50/30 to-purple-50/30 dark:from-gray-950 dark:via-indigo-950/30 dark:to-purple-950/30">
      {/* Animated gradient orbs */}
      <motion.div
        className="absolute -top-40 -left-40 w-96 h-96 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-full opacity-20 dark:opacity-10 blur-3xl"
        animate={{
          x: [0, 100, 0],
          y: [0, 50, 0],
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          repeatType: 'reverse',
        }}
      />
      
      <motion.div
        className="absolute top-1/4 -right-40 w-96 h-96 bg-gradient-to-r from-violet-400 to-fuchsia-400 rounded-full opacity-20 dark:opacity-10 blur-3xl"
        animate={{
          x: [0, -80, 0],
          y: [0, 100, 0],
          scale: [1, 1.3, 1],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          repeatType: 'reverse',
        }}
      />

      <motion.div
        className="absolute bottom-1/4 -left-20 w-80 h-80 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-full opacity-20 dark:opacity-10 blur-3xl"
        animate={{
          x: [0, 120, 0],
          y: [0, -80, 0],
          scale: [1, 1.4, 1],
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          repeatType: 'reverse',
        }}
      />

      <motion.div
        className="absolute -bottom-40 -right-20 w-96 h-96 bg-gradient-to-r from-violet-400 to-indigo-400 rounded-full opacity-20 dark:opacity-10 blur-3xl"
        animate={{
          x: [0, -60, 0],
          y: [0, -100, 0],
          scale: [1, 1.25, 1],
        }}
        transition={{
          duration: 22,
          repeat: Infinity,
          repeatType: 'reverse',
        }}
      />

      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-indigo-400 via-purple-400 to-violet-400 rounded-full opacity-10 dark:opacity-5 blur-3xl"
        animate={{
          rotate: 360,
          scale: [1, 1.1, 1],
        }}
        transition={{
          rotate: { duration: 50, repeat: Infinity, ease: 'linear' },
          scale: { duration: 8, repeat: Infinity, repeatType: 'reverse' },
        }}
      />

      {/* Floating particles */}
      {PARTICLES.map((p, i) => (
        <motion.div
          key={i}
          className={`absolute w-1 h-1 rounded-full ${p.colorClass} opacity-40 dark:opacity-20`}
          style={{
            left: p.left,
            top: p.top,
          }}
          animate={{
            y: [0, -30, 0],
            x: [0, p.animateX, 0],
            opacity: [0.4, 0.8, 0.4],
            scale: [1, 1.5, 1],
          }}
          transition={{
            duration: p.duration,
            repeat: Infinity,
            delay: p.delay,
          }}
        />
      ))}

      {/* Grid pattern overlay */}
      <div 
        className="absolute inset-0 opacity-[0.02] dark:opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(rgba(139, 92, 246, 0.3) 1px, transparent 1px),
                           linear-gradient(90deg, rgba(139, 92, 246, 0.3) 1px, transparent 1px)`,
          backgroundSize: '50px 50px',
        }}
      />

      {/* Radial gradient overlay */}
      <div className="absolute inset-0 bg-gradient-radial from-transparent via-transparent to-white/50 dark:to-black/50" />
    </div>
  );
};

export default MotionBg;
