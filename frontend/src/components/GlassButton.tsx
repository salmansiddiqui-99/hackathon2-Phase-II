import React from 'react';

interface GlassButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
  fullWidth?: boolean;
  gradient?: boolean;
}

export default function GlassButton({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  icon,
  fullWidth = false,
  gradient = true,
  className = '',
  ...props
}: GlassButtonProps) {
  const baseClasses = `
    flex
    items-center
    justify-center
    gap-2
    border
    border-transparent
    font-medium
    focus:outline-none
    focus:ring-2
    focus:ring-offset-2
    transition-all
    duration-200
    disabled:opacity-50
    disabled:cursor-not-allowed
    ${fullWidth ? 'w-full' : ''}
    ${gradient ? 'bg-gradient-to-r' : 'bg-white/10 backdrop-blur-sm border-white/20 text-white'}
    ${size === 'sm' ? 'py-2 px-4 text-sm rounded-lg' : ''}
    ${size === 'md' ? 'py-3 px-4 text-base rounded-xl' : ''}
    ${size === 'lg' ? 'py-4 px-6 text-lg rounded-xl' : ''}
  `;

  const variantClasses = gradient
    ? {
        primary: 'from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:ring-blue-500 shadow-lg hover:shadow-xl',
        secondary: 'from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 focus:ring-gray-500 shadow-lg hover:shadow-xl',
        success: 'from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 focus:ring-green-500 shadow-lg hover:shadow-xl',
        warning: 'from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 focus:ring-yellow-500 shadow-lg hover:shadow-xl',
        error: 'from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 focus:ring-red-500 shadow-lg hover:shadow-xl',
        ghost: 'bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 focus:ring-white/50 shadow-lg hover:shadow-xl'
      }
    : {
        primary: 'bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 focus:ring-white/50 shadow-lg hover:shadow-xl',
        secondary: 'bg-gray-500/10 backdrop-blur-sm border-gray-500/20 text-gray-100 hover:bg-gray-500/20 focus:ring-gray-500/50 shadow-lg hover:shadow-xl',
        success: 'bg-green-500/10 backdrop-blur-sm border-green-500/20 text-green-100 hover:bg-green-500/20 focus:ring-green-500/50 shadow-lg hover:shadow-xl',
        warning: 'bg-yellow-500/10 backdrop-blur-sm border-yellow-500/20 text-yellow-100 hover:bg-yellow-500/20 focus:ring-yellow-500/50 shadow-lg hover:shadow-xl',
        error: 'bg-red-500/10 backdrop-blur-sm border-red-500/20 text-red-100 hover:bg-red-500/20 focus:ring-red-500/50 shadow-lg hover:shadow-xl',
        ghost: 'bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white/20 focus:ring-white/50 shadow-lg hover:shadow-xl'
      };

  const finalClasses = `${baseClasses} ${variantClasses[variant]} ${className}`;

  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={finalClasses}
    >
      {loading ? (
        <>
          <svg
            className="animate-spin h-5 w-5 text-white"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>Loading...</span>
        </>
      ) : (
        <>
          {icon && icon}
          <span>{children}</span>
        </>
      )}
    </button>
  );
}