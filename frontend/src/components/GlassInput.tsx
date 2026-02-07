import React, { InputHTMLAttributes } from 'react';

interface GlassInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  icon?: React.ReactNode;
  error?: string;
  success?: boolean;
  variant?: 'default' | 'small' | 'large';
}

export default function GlassInput({
  label,
  icon,
  error,
  success,
  variant = 'default',
  className = '',
  ...props
}: GlassInputProps) {
  const sizeClasses = {
    small: 'py-2 px-4 text-sm',
    default: 'py-3 px-4',
    large: 'py-4 px-4 text-lg'
  };

  const baseClasses = `
    w-full
    bg-white/10
    backdrop-blur-sm
    border
    border-white/20
    rounded-xl
    text-white
    placeholder-gray-400
    focus:outline-none
    focus:ring-2
    focus:ring-blue-500
    focus:border-transparent
    transition-all
    duration-200
    appearance-none
    ${sizeClasses[variant]}
    ${icon ? 'pl-12' : 'pl-4'}
    ${error ? 'border-red-500/50 focus:ring-red-500' : ''}
    ${success ? 'border-green-500/50 focus:ring-green-500' : ''}
    ${className}
  `;

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-gray-300 mb-2">
          {label}
        </label>
      )}
      <div className="relative">
        {icon && (
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            {icon}
          </div>
        )}
        <input
          {...props}
          className={baseClasses}
        />
      </div>
      {error && (
        <p className="mt-1 text-sm text-red-400">{error}</p>
      )}
      {success && !error && (
        <p className="mt-1 text-sm text-green-400">Valid input</p>
      )}
    </div>
  );
}