'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { Mail, Lock, LogIn, Eye, EyeOff, Sparkles, AlertCircle } from 'lucide-react';
import GlassCard from '@/components/GlassCard';
import GlassInput from '@/components/GlassInput';
import GlassButton from '@/components/GlassButton';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await apiClient.login(email, password);

      // Store token in localStorage (in a real app, consider more secure storage)
      localStorage.setItem('token', data.access_token);

      // Redirect to dashboard or home page
      router.push('/tasks');
      router.refresh(); // Refresh to update auth state
    } catch (err: any) {
      setError(err.message || 'An error occurred during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden py-12 px-4 sm:px-6 lg:px-8">
      {/* Animated gradient background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" />

      {/* Floating gradient orbs */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '0s', animationDuration: '8s' }} />
      <div className="absolute top-1/3 right-0 w-80 h-80 bg-gradient-to-br from-purple-400/20 to-pink-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '2s', animationDuration: '10s' }} />
      <div className="absolute bottom-0 left-1/4 w-72 h-72 bg-gradient-to-br from-pink-400/20 to-blue-400/20 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '4s', animationDuration: '12s' }} />

      <div className="max-w-md w-full space-y-8 animate-in fade-in zoom-in-95 duration-500 relative z-10">
        {/* Header with glassmorphism */}
        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white/10 backdrop-blur-md rounded-2xl shadow-lg mb-4 border border-white/20">
            <Sparkles className="h-8 w-8 text-white" aria-hidden="true" />
          </div>
          <h2 className="text-4xl font-bold text-white mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Welcome Back
          </h2>
          <p className="text-base text-gray-300">
            Sign in to continue your productivity journey
          </p>
        </div>

        {/* Login form card with enhanced glassmorphism */}
        <GlassCard className="overflow-hidden">
          <form className="p-8 space-y-6" onSubmit={handleSubmit}>
            {/* Error message */}
            {error && (
              <GlassCard variant="error" className="animate-in fade-in slide-in-from-top-2">
                <div className="flex items-start gap-3 p-4">
                  <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-red-300">Authentication Error</h3>
                    <p className="text-sm text-red-200 mt-1">{error}</p>
                  </div>
                </div>
              </GlassCard>
            )}

            {/* Email field */}
            <GlassInput
              id="email-address"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              label="Email Address"
              icon={<Mail className="h-5 w-5 text-gray-400" aria-hidden="true" />}
              placeholder="you@example.com"
              aria-label="Email address"
            />

            {/* Password field */}
            <div className="relative">
              <GlassInput
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                label="Password"
                icon={<Lock className="h-5 w-5 text-gray-400" aria-hidden="true" />}
                placeholder="Enter your password"
                aria-label="Password"
              />

              {/* Password visibility toggle */}
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 px-3 py-2 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r-xl"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? (
                  <EyeOff className="h-5 w-5" aria-hidden="true" />
                ) : (
                  <Eye className="h-5 w-5" aria-hidden="true" />
                )}
              </button>
            </div>

            {/* Remember me and forgot password */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-white/20 rounded bg-white/10 backdrop-blur-sm"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-300">
                  Remember me
                </label>
              </div>

              <div className="text-sm">
                <a
                  href="#"
                  className="font-medium text-blue-400 hover:text-blue-300 transition-colors"
                >
                  Forgot password?
                </a>
              </div>
            </div>

            {/* Submit button */}
            <div>
              <GlassButton
                type="submit"
                disabled={loading}
                loading={loading}
                icon={<LogIn className="h-5 w-5" aria-hidden="true" />}
                fullWidth
              >
                Sign In
              </GlassButton>
            </div>
          </form>
        </GlassCard>

        {/* Sign up link */}
        <div className="text-center">
          <p className="text-sm text-gray-300">
            Don't have an account?{' '}
            <Link
              href="/register"
              className="font-semibold text-blue-400 hover:text-blue-300 transition-colors"
            >
              Sign up for free
            </Link>
          </p>
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-gray-500">
          <p>Secure authentication powered by JWT</p>
        </div>
      </div>
    </div>
  );
}