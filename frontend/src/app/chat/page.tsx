'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import ChatKit from '../../components/ChatKit/ChatKit';
import LoadingSpinner from '../../components/LoadingSpinner';
import { Bot, Sparkles, ListTodo, RefreshCw } from 'lucide-react';
import ProtectedLayout from '../../components/ProtectedLayout';
import GlassCard from '../../components/GlassCard';

export default function ChatPage() {
  const [userId, setUserId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Extract user ID from the JWT token stored in localStorage
  const getTokenUserId = (): number => {
    if (typeof window === 'undefined') return 1; // Fallback for SSR

    const token = localStorage.getItem('token');
    if (!token) {
      // Redirect to login if no token
      router.push('/login');
      return 1;
    }

    try {
      // Decode JWT token to get user ID
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid token format');
      }

      const payload = JSON.parse(atob(parts[1]));
      return parseInt(payload.sub, 10);
    } catch (error) {
      console.error('Error decoding token:', error);
      // Redirect to login if token is invalid
      router.push('/login');
      return 1;
    }
  };

  useEffect(() => {
    const userId = getTokenUserId();
    setUserId(userId);
    setLoading(false);
  }, []);

  const handleRefresh = () => {
    window.location.reload();
  };

  if (loading) {
    return (
      <ProtectedLayout>
        <div className="min-h-screen flex items-center justify-center p-6">
          <LoadingSpinner message="Initializing chat..." size="lg" />
        </div>
      </ProtectedLayout>
    );
  }

  return (
    <ProtectedLayout>
      <div className="p-6 min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
        {/* Page title */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-white/10 backdrop-blur-md rounded-xl shadow-lg border border-white/20">
              <Bot className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">AI Chat Assistant</h1>
              <p className="text-sm text-gray-300">Manage your tasks with natural language</p>
            </div>
          </div>
        </div>

        {/* Welcome card */}
        <GlassCard className="mb-6">
          <div className="p-6 text-center">
            <div className="max-w-2xl mx-auto">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-white/10 backdrop-blur-md rounded-full mb-4 border border-white/20">
                <Sparkles className="h-8 w-8 text-white" aria-hidden="true" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Welcome to AI Task Assistant
              </h3>
              <p className="text-gray-300">
                Use natural language to manage your tasks. Tell me to create, update, complete, or delete tasks.
              </p>
            </div>
          </div>
        </GlassCard>

        {/* Chat container with glassmorphism */}
        <GlassCard className="p-4 h-[calc(100vh-250px)] max-h-[600px]">
          {userId && <ChatKit userId={userId} />}
        </GlassCard>
      </div>
    </ProtectedLayout>
  );
}