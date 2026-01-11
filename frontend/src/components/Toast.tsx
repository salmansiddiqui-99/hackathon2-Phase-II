import React, { useEffect, useState } from 'react';
import { CheckCircle2, XCircle, AlertTriangle, Info, X } from 'lucide-react';

interface ToastProps {
  message: string;
  type?: 'success' | 'error' | 'warning' | 'info';
  duration?: number;
  onClose: () => void;
}

const Toast: React.FC<ToastProps> = ({ message, type = 'info', duration = 3000, onClose }) => {
  const [isExiting, setIsExiting] = useState(false);
  const [progress, setProgress] = useState(100);

  useEffect(() => {
    // Progress bar animation
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev <= 0) return 0;
        return prev - (100 / (duration / 50));
      });
    }, 50);

    // Auto-close timer
    const closeTimer = setTimeout(() => {
      setIsExiting(true);
      setTimeout(onClose, 300); // Wait for exit animation
    }, duration);

    return () => {
      clearTimeout(closeTimer);
      clearInterval(progressInterval);
    };
  }, [duration, onClose]);

  const handleClose = () => {
    setIsExiting(true);
    setTimeout(onClose, 300);
  };

  // Type-specific configuration
  const getTypeConfig = () => {
    switch (type) {
      case 'success':
        return {
          icon: <CheckCircle2 className="h-5 w-5" aria-hidden="true" />,
          bgColor: 'bg-gradient-to-r from-green-500 to-emerald-600',
          textColor: 'text-white',
          iconColor: 'text-white',
          progressColor: 'bg-green-200'
        };
      case 'error':
        return {
          icon: <XCircle className="h-5 w-5" aria-hidden="true" />,
          bgColor: 'bg-gradient-to-r from-red-500 to-rose-600',
          textColor: 'text-white',
          iconColor: 'text-white',
          progressColor: 'bg-red-200'
        };
      case 'warning':
        return {
          icon: <AlertTriangle className="h-5 w-5" aria-hidden="true" />,
          bgColor: 'bg-gradient-to-r from-yellow-400 to-orange-500',
          textColor: 'text-gray-900',
          iconColor: 'text-gray-900',
          progressColor: 'bg-yellow-200'
        };
      case 'info':
      default:
        return {
          icon: <Info className="h-5 w-5" aria-hidden="true" />,
          bgColor: 'bg-gradient-to-r from-blue-500 to-indigo-600',
          textColor: 'text-white',
          iconColor: 'text-white',
          progressColor: 'bg-blue-200'
        };
    }
  };

  const config = getTypeConfig();

  return (
    <div
      role="alert"
      aria-live="polite"
      aria-atomic="true"
      className={`fixed bottom-6 right-6 z-50 transition-all duration-300 transform ${
        isExiting
          ? 'translate-x-full opacity-0'
          : 'translate-x-0 opacity-100'
      }`}
    >
      <div
        className={`${config.bgColor} ${config.textColor} rounded-xl shadow-2xl overflow-hidden min-w-[320px] max-w-md backdrop-blur-sm`}
      >
        {/* Main content */}
        <div className="flex items-start gap-3 p-4">
          {/* Icon */}
          <div className={`flex-shrink-0 ${config.iconColor}`}>
            {config.icon}
          </div>

          {/* Message */}
          <p className="flex-1 text-sm font-medium leading-relaxed pt-0.5">
            {message}
          </p>

          {/* Close button */}
          <button
            onClick={handleClose}
            className={`flex-shrink-0 ${config.textColor} hover:opacity-70 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-transparent rounded-lg p-1 transition-opacity`}
            aria-label="Close notification"
          >
            <X className="h-4 w-4" aria-hidden="true" />
          </button>
        </div>

        {/* Progress bar */}
        <div className={`h-1 ${config.progressColor} bg-opacity-30`}>
          <div
            className={`h-full ${config.progressColor} transition-all duration-50 ease-linear`}
            style={{ width: `${progress}%` }}
            role="progressbar"
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label="Time remaining"
          />
        </div>
      </div>
    </div>
  );
};

export default Toast;