'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { apiClient } from '../../../lib/api';
import { Task } from '../../../types';

export default function IndividualTaskPage() {
  const { id } = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  // For demo purposes, we'll use a fixed user ID
  // In a real app, this would come from the authenticated user context
  const userId = 1;

  useEffect(() => {
    if (id) {
      fetchTask(Number(id));
    }
  }, [id]);

  const fetchTask = async (taskId: number) => {
    try {
      setLoading(true);
      const taskData = await apiClient.getTaskById(userId, taskId);
      setTask(taskData);
      setEditTitle(taskData.title);
      setEditDescription(taskData.description || '');
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateTask = async () => {
    if (!task) return;

    try {
      const updatedTask = await apiClient.updateTask(userId, task.id, {
        title: editTitle,
        description: editDescription,
      });
      setTask(updatedTask);
      setIsEditing(false);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleToggleComplete = async () => {
    if (!task) return;

    try {
      const updatedTask = await apiClient.toggleTaskCompletion(userId, task.id);
      setTask(updatedTask);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleDeleteTask = async () => {
    if (!task) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await apiClient.deleteTask(userId, task.id);
        router.push('/tasks');
      } catch (err) {
        setError((err as Error).message);
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading task...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-red-500">Error: {error}</div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Task not found</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6">
        <div className="flex justify-between items-start">
          <h1 className="text-2xl font-bold mb-4">Task Details</h1>
          <button
            onClick={() => router.push('/tasks')}
            className="text-indigo-600 hover:text-indigo-900"
          >
            ← Back to Tasks
          </button>
        </div>

        {isEditing ? (
          <div className="space-y-4">
            <div>
              <label htmlFor="edit-title" className="block text-sm font-medium text-gray-700 mb-1">
                Title
              </label>
              <input
                id="edit-title"
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label htmlFor="edit-description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="edit-description"
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div className="flex space-x-2">
              <button
                onClick={handleUpdateTask}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Save Changes
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div>
              <h2 className={`text-xl font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h2>
            </div>

            {task.description && (
              <div className="prose">
                <p>{task.description}</p>
              </div>
            )}

            <div className="flex items-center space-x-4">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                task.completed
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}>
                {task.completed ? 'Completed' : 'Pending'}
              </span>
              <span className="text-sm text-gray-500">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </span>
            </div>

            <div className="flex space-x-3 pt-4">
              <button
                onClick={handleToggleComplete}
                className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
                  task.completed
                    ? 'bg-yellow-600 hover:bg-yellow-700'
                    : 'bg-green-600 hover:bg-green-700'
                } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500`}
              >
                {task.completed ? 'Mark as Pending' : 'Mark as Complete'}
              </button>

              <button
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Edit
              </button>

              <button
                onClick={handleDeleteTask}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                Delete
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}