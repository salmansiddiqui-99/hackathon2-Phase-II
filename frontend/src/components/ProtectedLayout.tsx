'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import SidebarLayout from '../components/SidebarLayout';
import LoadingSpinner from '../components/LoadingSpinner';

interface ProtectedLayoutProps {
  children: React.ReactNode;
}

export default function ProtectedLayout({ children }: ProtectedLayoutProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = () => {
      // Check if user is authenticated by looking for the token in localStorage
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

      if (token) {
        // In a real app, you might want to validate the token with the server
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
        // Redirect to login page
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  if (isAuthenticated === null) {
    // Loading state while checking authentication
    return (
      <div className="min-h-screen flex items-center justify-center p-6 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        <LoadingSpinner message="Checking authentication..." size="lg" />
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect is happening in the effect, but we return null here to prevent rendering
    return null;
  }

  // User is authenticated, render the sidebar layout with protected content
  return <SidebarLayout>{children}</SidebarLayout>;
}