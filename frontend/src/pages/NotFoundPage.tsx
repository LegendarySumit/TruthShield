
import { Link } from 'react-router-dom';
import Footer from '../components/Footer';

const NotFoundPage = () => {
  return (
    <div className="text-center py-12 sm:py-16 md:py-20 px-3 xs:px-4 sm:px-6 lg:px-8">
      <h1 className="text-3xl xs:text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 dark:text-white">404</h1>
      <p className="mt-3 sm:mt-4 max-w-2xl mx-auto text-base sm:text-lg md:text-xl text-gray-600 dark:text-gray-300">
        Page Not Found
      </p>
      <div className="mt-6 sm:mt-8">
        <Link 
          to="/"
          className="px-5 py-2.5 xs:px-6 sm:px-8 sm:py-3 bg-indigo-600 text-white font-semibold text-sm sm:text-base rounded-lg shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-75"
        >
          Go back to Home
        </Link>
      </div>
      <Footer />
    </div>
  );
};

export default NotFoundPage;
