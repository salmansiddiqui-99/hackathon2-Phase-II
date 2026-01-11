import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  fullScreen?: boolean;
}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  size = 'md',
  fullScreen = false
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  };

  const containerClasses = fullScreen
    ? 'fixed inset-0 flex flex-col items-center justify-center bg-white bg-opacity-90 z-50'
    : 'flex flex-col items-center justify-center py-8';

  return (
    <div className={containerClasses} role="status" aria-live="polite">
      {/* Animated gradient background pulse */}
      <div className="relative">
        {/* Outer pulsing ring */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 opacity-20 animate-ping" />

        {/* Middle rotating ring */}
        <div className="absolute inset-0 rounded-full border-4 border-transparent border-t-indigo-500 border-r-purple-500 animate-spin" style={{ animationDuration: '1.5s' }} />

        {/* Inner icon spinner */}
        <div className="relative">
          <Loader2
            className={`${sizeClasses[size]} text-indigo-600 animate-spin`}
            aria-hidden="true"
            style={{ animationDuration: '1s' }}
          />
        </div>
      </div>

      {/* Loading message with typing animation */}
      {message && (
        <div className="mt-6 text-center space-y-2">
          <p className="text-base font-medium text-gray-700 animate-pulse">
            {message}
          </p>
          {/* Animated dots */}
          <div className="flex items-center justify-center gap-1">
            <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <span className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <span className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        </div>
      )}

      {/* Screen reader text */}
      <span className="sr-only">{message}</span>
    </div>
  );
};

export default LoadingSpinner;