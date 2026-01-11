'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '../../lib/api';
import TaskForm from '../../components/TaskForm';
import TaskList from '../../components/TaskList';
import LoadingSpinner from '../../components/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage';
import { Task } from '../../types';
import { ListTodo, CheckCircle2, Circle, Sparkles, LogOut, RefreshCw } from 'lucide-react';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  // Extract user ID from the JWT token stored in localStorage
  const getTokenUserId = (): number => {
    if (typeof window === 'undefined') return 1; // Fallback for SSR

    const token = localStorage.getItem('token');
    if (!token) {
      // Redirect to login if no token
      window.location.href = '/login';
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
      window.location.href = '/login';
      return 1;
    }
  };

  const userId = getTokenUserId();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const tasksData = await apiClient.getTasks(userId);
      setTasks(tasksData);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title: string, description: string) => {
    try {
      const newTask = await apiClient.createTask(userId, { title, description });
      setTasks([newTask, ...tasks]); // Add new task at the beginning
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleUpdateTask = async (id: number, title: string, description: string) => {
    try {
      const updatedTask = await apiClient.updateTask(userId, id, { title, description });
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      setEditingTask(null);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await apiClient.deleteTask(userId, id);
      setTasks(tasks.filter(task => task.id !== id));
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleToggleComplete = async (id: number) => {
    try {
      const updatedTask = await apiClient.toggleTaskCompletion(userId, id);
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const startEditing = (task: Task) => {
    setEditingTask(task);
  };

  const cancelEditing = () => {
    setEditingTask(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  const handleRetry = () => {
    fetchTasks();
  };

  // Calculate statistics
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = tasks.length - completedTasks;
  const completionPercentage = tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
        <LoadingSpinner message="Loading your tasks..." size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {/* Header with gradient */}
      <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-40 backdrop-blur-sm bg-opacity-90">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl shadow-lg">
                <ListTodo className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
                <p className="text-sm text-gray-600">Organize your day with ease</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={handleRetry}
                className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border-2 border-gray-300 rounded-xl hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200 hover:scale-105"
                aria-label="Refresh tasks"
              >
                <RefreshCw className="h-4 w-4" aria-hidden="true" />
                <span className="hidden sm:inline">Refresh</span>
              </button>
              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-red-500 to-rose-600 rounded-xl hover:from-red-600 hover:to-rose-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 shadow-lg transition-all duration-200 hover:scale-105"
                aria-label="Logout"
              >
                <LogOut className="h-4 w-4" aria-hidden="true" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error message */}
        {error && (
          <div className="mb-6 animate-in fade-in slide-in-from-top-4">
            <ErrorMessage message={error} onClose={() => setError(null)} />
          </div>
        )}

        {/* Statistics cards */}
        {tasks.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8 animate-in fade-in slide-in-from-top-4">
            {/* Total tasks */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow duration-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">{tasks.length}</p>
                </div>
                <div className="p-3 bg-indigo-100 rounded-lg">
                  <ListTodo className="h-6 w-6 text-indigo-600" aria-hidden="true" />
                </div>
              </div>
            </div>

            {/* Pending tasks */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow duration-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Pending</p>
                  <p className="text-3xl font-bold text-orange-600 mt-1">{pendingTasks}</p>
                </div>
                <div className="p-3 bg-orange-100 rounded-lg">
                  <Circle className="h-6 w-6 text-orange-600" aria-hidden="true" />
                </div>
              </div>
            </div>

            {/* Completed tasks */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-5 hover:shadow-md transition-shadow duration-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Completed</p>
                  <p className="text-3xl font-bold text-green-600 mt-1">{completedTasks}</p>
                </div>
                <div className="p-3 bg-green-100 rounded-lg">
                  <CheckCircle2 className="h-6 w-6 text-green-600" aria-hidden="true" />
                </div>
              </div>
              {/* Progress bar */}
              <div className="mt-3">
                <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                  <span>Progress</span>
                  <span className="font-semibold">{completionPercentage}%</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-500 to-emerald-600 transition-all duration-500 ease-out"
                    style={{ width: `${completionPercentage}%` }}
                    role="progressbar"
                    aria-valuenow={completionPercentage}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-label="Task completion progress"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Task form */}
        <TaskForm
          onCreate={handleCreateTask}
          onUpdate={handleUpdateTask}
          editingTask={editingTask}
          onCancelEdit={cancelEditing}
        />

        {/* Task list or empty state */}
        <div className="mb-6">
          {tasks.length === 0 ? (
            // Beautiful empty state
            <div className="bg-white rounded-2xl shadow-sm border-2 border-dashed border-gray-300 p-12 text-center animate-in fade-in zoom-in-95 duration-500">
              <div className="max-w-md mx-auto">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-full mb-6 animate-pulse">
                  <Sparkles className="h-10 w-10 text-white" aria-hidden="true" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-3">
                  No tasks yet
                </h3>
                <p className="text-gray-600 mb-6 leading-relaxed">
                  Start your productivity journey by creating your first task. Break down your goals into manageable steps and watch your progress grow!
                </p>
                <div className="inline-flex items-center gap-2 text-sm text-indigo-600 font-medium">
                  <span>Use the form above to get started</span>
                  <svg className="h-5 w-5 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                  </svg>
                </div>
              </div>
            </div>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  Your Tasks
                </h2>
                <span className="text-sm text-gray-600 bg-white px-3 py-1 rounded-full border border-gray-200">
                  {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                </span>
              </div>
              <TaskList
                tasks={tasks}
                onToggleComplete={handleToggleComplete}
                onDelete={handleDeleteTask}
                onUpdate={handleUpdateTask}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}