import React from 'react';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  elevated?: boolean;
  rounded?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
}

export default function GlassCard({
  children,
  className = '',
  variant = 'default',
  elevated = true,
  rounded = 'xl'
}: GlassCardProps) {
  const variantClasses = {
    default: 'bg-white/10 backdrop-blur-xl border-white/20 text-white',
    primary: 'bg-blue-500/10 backdrop-blur-xl border-blue-500/20 text-blue-100',
    secondary: 'bg-purple-500/10 backdrop-blur-xl border-purple-500/20 text-purple-100',
    success: 'bg-green-500/10 backdrop-blur-xl border-green-500/20 text-green-100',
    warning: 'bg-yellow-500/10 backdrop-blur-xl border-yellow-500/20 text-yellow-100',
    error: 'bg-red-500/10 backdrop-blur-xl border-red-500/20 text-red-100'
  };

  const elevationClasses = elevated
    ? 'shadow-xl hover:shadow-2xl transition-shadow duration-300'
    : 'shadow-lg';

  const roundedClasses = {
    sm: 'rounded-sm',
    md: 'rounded-md',
    lg: 'rounded-lg',
    xl: 'rounded-xl',
    '2xl': 'rounded-2xl',
    full: 'rounded-full'
  };

  return (
    <div
      className={`
        ${variantClasses[variant]}
        ${elevationClasses}
        ${roundedClasses[rounded]}
        border
        overflow-hidden
        ${className}
      `}
    >
      {children}
    </div>
  );
}