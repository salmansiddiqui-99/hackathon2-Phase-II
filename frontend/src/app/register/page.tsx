'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import { Mail, Lock, UserPlus, Eye, EyeOff, Sparkles, AlertCircle, CheckCircle2 } from 'lucide-react';
import GlassCard from '@/components/GlassCard';
import GlassInput from '@/components/GlassInput';
import GlassButton from '@/components/GlassButton';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const router = useRouter();

  // Password strength validation
  const getPasswordStrength = (pass: string): { strength: number; label: string; color: string } => {
    let strength = 0;
    if (pass.length >= 8) strength++;
    if (pass.match(/[a-z]/) && pass.match(/[A-Z]/)) strength++;
    if (pass.match(/\d/)) strength++;
    if (pass.match(/[^a-zA-Z\d]/)) strength++;

    if (strength === 0 || pass.length === 0) return { strength: 0, label: '', color: '' };
    if (strength <= 1) return { strength: 25, label: 'Weak', color: 'bg-red-500' };
    if (strength === 2) return { strength: 50, label: 'Fair', color: 'bg-orange-500' };
    if (strength === 3) return { strength: 75, label: 'Good', color: 'bg-yellow-500' };
    return { strength: 100, label: 'Strong', color: 'bg-green-500' };
  };

  const passwordStrength = getPasswordStrength(password);
  const passwordsMatch = password && confirmPassword && password === confirmPassword;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await apiClient.register(email, password);

      // Store token in localStorage (in a real app, consider more secure storage)
      localStorage.setItem('token', data.access_token);

      // Redirect to dashboard or home page
      router.push('/tasks');
      router.refresh(); // Refresh to update auth state
    } catch (err: any) {
      setError(err.message || 'An error occurred during registration');
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
            Create Account
          </h2>
          <p className="text-base text-gray-300">
            Start organizing your tasks today
          </p>
        </div>

        {/* Register form card with enhanced glassmorphism */}
        <GlassCard className="overflow-hidden">
          <form className="p-8 space-y-6" onSubmit={handleSubmit}>
            {/* Error message */}
            {error && (
              <GlassCard variant="error" className="animate-in fade-in slide-in-from-top-2">
                <div className="flex items-start gap-3 p-4">
                  <AlertCircle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" aria-hidden="true" />
                  <div className="flex-1">
                    <h3 className="text-sm font-medium text-red-300">Registration Error</h3>
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
                autoComplete="new-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                label="Password"
                icon={<Lock className="h-5 w-5 text-gray-400" aria-hidden="true" />}
                placeholder="Create a strong password"
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

              {/* Password strength indicator */}
              {password && (
                <div className="mt-2 animate-in fade-in slide-in-from-top-1">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="text-gray-400">Password strength</span>
                    <span className={`font-semibold ${
                      passwordStrength.strength === 100 ? 'text-green-400' :
                      passwordStrength.strength >= 50 ? 'text-yellow-400' : 'text-red-400'
                    }`}>
                      {passwordStrength.label}
                    </span>
                  </div>
                  <div className="h-2 bg-white/10 rounded-full overflow-hidden backdrop-blur-sm">
                    <div
                      className={`h-full ${passwordStrength.color} transition-all duration-300`}
                      style={{ width: `${passwordStrength.strength}%` }}
                      role="progressbar"
                      aria-valuenow={passwordStrength.strength}
                      aria-valuemin={0}
                      aria-valuemax={100}
                      aria-label="Password strength"
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Confirm Password field */}
            <div className="relative">
              <GlassInput
                id="confirm-password"
                name="confirm-password"
                type={showConfirmPassword ? 'text' : 'password'}
                autoComplete="new-password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                label="Confirm Password"
                icon={<Lock className="h-5 w-5 text-gray-400" aria-hidden="true" />}
                placeholder="Confirm your password"
                aria-label="Confirm password"
              />

              {/* Password visibility toggle */}
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 px-3 py-2 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-r-xl"
                aria-label={showConfirmPassword ? 'Hide password' : 'Show password'}
              >
                {showConfirmPassword ? (
                  <EyeOff className="h-5 w-5" aria-hidden="true" />
                ) : (
                  <Eye className="h-5 w-5" aria-hidden="true" />
                )}
              </button>

              {/* Password match indicator */}
              {confirmPassword && (
                <div className="mt-2 animate-in fade-in slide-in-from-top-1">
                  {passwordsMatch ? (
                    <div className="flex items-center gap-2 text-sm text-green-400">
                      <CheckCircle2 className="h-4 w-4" aria-hidden="true" />
                      <span>Passwords match</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-sm text-red-400">
                      <AlertCircle className="h-4 w-4" aria-hidden="true" />
                      <span>Passwords do not match</span>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Submit button */}
            <div className="pt-2">
              <GlassButton
                type="submit"
                disabled={loading || (!!confirmPassword && !passwordsMatch)}
                loading={loading}
                icon={<UserPlus className="h-5 w-5" aria-hidden="true" />}
                fullWidth
              >
                Create Account
              </GlassButton>
            </div>

            {/* Terms notice */}
            <p className="text-xs text-center text-gray-400">
              By signing up, you agree to our{' '}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                Terms of Service
              </a>{' '}
              and{' '}
              <a href="#" className="text-blue-400 hover:text-blue-300">
                Privacy Policy
              </a>
            </p>
          </form>
        </GlassCard>

        {/* Sign in link */}
        <div className="text-center">
          <p className="text-sm text-gray-300">
            Already have an account?{' '}
            <Link
              href="/login"
              className="font-semibold text-blue-400 hover:text-blue-300 transition-colors"
            >
              Sign in instead
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