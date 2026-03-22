import { useEffect, useState } from 'react';
import { trackEvent } from '../lib/analytics';

const OfflineBanner = () => {
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  useEffect(() => {
    const onOffline = () => {
      setIsOffline(true);
      trackEvent('offline_detected');
    };
    const onOnline = () => {
      setIsOffline(false);
      trackEvent('online_restored');
    };

    window.addEventListener('offline', onOffline);
    window.addEventListener('online', onOnline);

    return () => {
      window.removeEventListener('offline', onOffline);
      window.removeEventListener('online', onOnline);
    };
  }, []);

  if (!isOffline) {
    return null;
  }

  return (
    <div className="fixed top-16 left-0 right-0 z-50 px-3">
      <div className="mx-auto max-w-4xl rounded-lg border border-amber-300 bg-amber-100 px-4 py-2 text-sm font-medium text-amber-900 shadow-md dark:border-amber-800 dark:bg-amber-900/80 dark:text-amber-100">
        You are offline. Requests will fail until your connection is restored.
      </div>
    </div>
  );
};

export default OfflineBanner;
