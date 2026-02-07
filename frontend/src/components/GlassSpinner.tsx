import React from 'react';

interface GlassSpinnerProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export default function GlassSpinner({ message, size = 'md', className = '' }: GlassSpinnerProps) {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  return (
    <div className={`flex flex-col items-center justify-center gap-3 ${className}`}>
      <div className={`${sizeClasses[size]} animate-spin rounded-full border-2 border-white/30 border-t-white`} />
      {message && (
        <p className="text-sm text-gray-300">{message}</p>
      )}
    </div>
  );
}