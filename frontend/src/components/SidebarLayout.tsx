'use client';

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import { ListTodo, Bot, LogOut, Menu, X } from 'lucide-react';

interface SidebarLayoutProps {
  children: React.ReactNode;
}

export default function SidebarLayout({ children }: SidebarLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const pathname = usePathname();

  const closeSidebar = () => setIsSidebarOpen(false);

  // Extract user ID from the JWT token stored in localStorage
  const getTokenUserId = (): number => {
    if (typeof window === 'undefined') return 1; // Fallback for SSR

    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/login';
      return 1;
    }

    try {
      const parts = token.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid token format');
      }

      const payload = JSON.parse(atob(parts[1]));
      return parseInt(payload.sub, 10);
    } catch (error) {
      console.error('Error decoding token:', error);
      window.location.href = '/login';
      return 1;
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  useEffect(() => {
    // Close sidebar when navigating to a new page
    setIsSidebarOpen(false);
  }, [pathname]);

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Mobile sidebar toggle button */}
      <button
        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        className="fixed top-4 left-4 z-50 md:hidden p-2 rounded-lg bg-white/10 backdrop-blur-md shadow-md text-white hover:bg-white/20 focus:outline-none focus:ring-2 focus:ring-blue-500 border border-white/20"
        aria-label={isSidebarOpen ? 'Close menu' : 'Open menu'}
      >
        {isSidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </button>

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-40 w-64 bg-white/10 backdrop-blur-xl shadow-lg transform transition-transform duration-300 ease-in-out border-r border-white/20 md:translate-x-0 ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } md:static md:translate-x-0`}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center gap-3 p-6 border-b border-white/20">
            <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg">
              <Bot className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Task Manager AI</h1>
              <p className="text-xs text-gray-300">AI-Powered Productivity</p>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4">
            <ul className="space-y-2">
              <li>
                <Link
                  href="/tasks"
                  onClick={closeSidebar}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-colors ${
                    pathname === '/tasks'
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                      : 'text-gray-300 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <ListTodo className="h-5 w-5" />
                  <span>My Tasks</span>
                </Link>
              </li>
              <li>
                <Link
                  href="/chat"
                  onClick={closeSidebar}
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-colors ${
                    pathname === '/chat'
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg'
                      : 'text-gray-300 hover:bg-white/10 hover:text-white'
                  }`}
                >
                  <Bot className="h-5 w-5" />
                  <span>AI Assistant</span>
                </Link>
              </li>
            </ul>
          </nav>

          {/* User info and logout */}
          <div className="p-4 border-t border-white/20">
            <div className="text-xs text-gray-400 mb-2">User ID: {getTokenUserId()}</div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-4 py-3 text-gray-300 bg-white/10 hover:bg-white/20 rounded-xl transition-colors backdrop-blur-sm border border-white/20"
            >
              <LogOut className="h-5 w-5" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black bg-opacity-50 md:hidden"
          onClick={closeSidebar}
        ></div>
      )}

      {/* Main content */}
      <main className="flex-1 overflow-auto backdrop-blur-sm">
        <div className="h-full">{children}</div>
      </main>
    </div>
  );
}