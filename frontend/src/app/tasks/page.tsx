'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '../../lib/api';
import TaskForm from '../../components/TaskForm';
import TaskList from '../../components/TaskList';
import LoadingSpinner from '../../components/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage';
import { Task } from '../../types';
import { ListTodo, CheckCircle2, Circle, RefreshCw, Sparkles } from 'lucide-react';
import ProtectedLayout from '../../components/ProtectedLayout';
import GlassCard from '../../components/GlassCard';

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
      const tasksData = await apiClient.getTasks();
      setTasks(tasksData);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title: string, description: string) => {
    try {
      const newTask = await apiClient.createTask({ title, description });
      setTasks([newTask, ...tasks]); // Add new task at the beginning
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleUpdateTask = async (id: number, title: string, description: string) => {
    try {
      const updatedTask = await apiClient.updateTask(id, { title, description });
      setTasks(tasks.map(task => task.id === id ? updatedTask : task));
      setEditingTask(null);
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await apiClient.deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
      setError(null);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleToggleComplete = async (id: number) => {
    try {
      const updatedTask = await apiClient.toggleTaskCompletion(id);
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

  const handleRetry = () => {
    fetchTasks();
  };

  // Calculate statistics
  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = tasks.length - completedTasks;
  const completionPercentage = tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0;

  if (loading) {
    return (
      <ProtectedLayout>
        <div className="min-h-screen flex items-center justify-center p-6">
          <LoadingSpinner message="Loading your tasks..." size="lg" />
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
              <ListTodo className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">My Tasks</h1>
              <p className="text-sm text-gray-300">Organize your day with ease</p>
            </div>
          </div>
        </div>

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
            <GlassCard>
              <div className="flex items-center justify-between p-5">
                <div>
                  <p className="text-sm font-medium text-gray-300">Total Tasks</p>
                  <p className="text-3xl font-bold text-white mt-1">{tasks.length}</p>
                </div>
                <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                  <ListTodo className="h-6 w-6 text-blue-400" aria-hidden="true" />
                </div>
              </div>
            </GlassCard>

            {/* Pending tasks */}
            <GlassCard>
              <div className="flex items-center justify-between p-5">
                <div>
                  <p className="text-sm font-medium text-gray-300">Pending</p>
                  <p className="text-3xl font-bold text-orange-400 mt-1">{pendingTasks}</p>
                </div>
                <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                  <Circle className="h-6 w-6 text-orange-400" aria-hidden="true" />
                </div>
              </div>
            </GlassCard>

            {/* Completed tasks */}
            <GlassCard>
              <div className="flex items-center justify-between p-5">
                <div>
                  <p className="text-sm font-medium text-gray-300">Completed</p>
                  <p className="text-3xl font-bold text-green-400 mt-1">{completedTasks}</p>
                </div>
                <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
                  <CheckCircle2 className="h-6 w-6 text-green-400" aria-hidden="true" />
                </div>
              </div>
              {/* Progress bar */}
              <div className="px-5 pb-5">
                <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
                  <span>Progress</span>
                  <span className="font-semibold text-white">{completionPercentage}%</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden backdrop-blur-sm">
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
            </GlassCard>
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
            // Beautiful empty state with glassmorphism
            <GlassCard className="p-12 text-center animate-in fade-in zoom-in-95 duration-500">
              <div className="max-w-md mx-auto">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-white/10 backdrop-blur-md rounded-full mb-6 border border-white/20">
                  <Sparkles className="h-10 w-10 text-white" aria-hidden="true" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-3 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  No tasks yet
                </h3>
                <p className="text-gray-300 mb-6 leading-relaxed">
                  Start your productivity journey by creating your first task. Break down your goals into manageable steps and watch your progress grow!
                </p>
                <div className="inline-flex items-center gap-2 text-sm text-blue-400 font-medium">
                  <span>Use the form above to get started</span>
                  <svg className="h-5 w-5 animate-bounce text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 10l7-7m0 0l7 7m-7-7v18" />
                  </svg>
                </div>
              </div>
            </GlassCard>
          ) : (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">
                  Your Tasks
                </h2>
                <span className="text-sm text-gray-300 bg-white/10 px-3 py-1 rounded-full border border-white/20 backdrop-blur-sm">
                  {tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}
                </span>
              </div>
              <GlassCard>
                <TaskList
                  tasks={tasks}
                  onToggleComplete={handleToggleComplete}
                  onDelete={handleDeleteTask}
                  onUpdate={handleUpdateTask}
                />
              </GlassCard>
            </div>
          )}
        </div>
      </div>
    </ProtectedLayout>
  );
}