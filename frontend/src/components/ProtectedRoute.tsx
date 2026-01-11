'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ReactNode } from 'react';

interface ProtectedRouteProps {
  children: ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
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
  }, [router]);

  if (isAuthenticated === null) {
    // Loading state while checking authentication
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Checking authentication...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect is happening in the effect, but we return null here to prevent rendering
    return null;
  }

  // User is authenticated, render the protected content
  return <>{children}</>;
}