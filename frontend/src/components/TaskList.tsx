'use client';

import { useState } from 'react';
import { Task } from '../types';
import { CheckCircle2, Circle, Edit2, Trash2, Save, X } from 'lucide-react';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (id: number) => void;
  onDelete: (id: number) => void;
  onUpdate: (id: number, title: string, description: string) => void;
}

export default function TaskList({ tasks, onToggleComplete, onDelete, onUpdate }: TaskListProps) {
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || '');
  };

  const saveEdit = (id: number) => {
    if (!editTitle.trim()) return;
    onUpdate(id, editTitle, editDescription);
    setEditingId(null);
  };

  const cancelEdit = () => {
    setEditingId(null);
  };

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent, id: number) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      saveEdit(id);
    } else if (e.key === 'Escape') {
      cancelEdit();
    }
  };

  return (
    <div className="space-y-3">
      {tasks.map((task, index) => (
        <div
          key={task.id}
          className="group relative bg-white rounded-xl shadow-sm hover:shadow-md border border-gray-200 hover:border-indigo-300 transition-all duration-200 animate-in fade-in slide-in-from-top-2"
          style={{ animationDelay: `${index * 50}ms` }}
        >
          {editingId === task.id ? (
            // Editing view with enhanced styling
            <div className="p-5 space-y-4">
              <div>
                <label htmlFor={`edit-title-${task.id}`} className="sr-only">
                  Edit task title
                </label>
                <input
                  id={`edit-title-${task.id}`}
                  type="text"
                  value={editTitle}
                  onChange={(e) => setEditTitle(e.target.value)}
                  onKeyDown={(e) => handleKeyDown(e, task.id)}
                  className="w-full px-4 py-2.5 text-base font-medium border-2 border-indigo-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                  placeholder="Task title"
                  autoFocus
                  aria-label="Task title"
                />
              </div>
              <div>
                <label htmlFor={`edit-description-${task.id}`} className="sr-only">
                  Edit task description
                </label>
                <textarea
                  id={`edit-description-${task.id}`}
                  value={editDescription}
                  onChange={(e) => setEditDescription(e.target.value)}
                  onKeyDown={(e) => handleKeyDown(e, task.id)}
                  className="w-full px-4 py-2.5 text-sm border-2 border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
                  placeholder="Task description (optional)"
                  rows={3}
                  aria-label="Task description"
                />
              </div>
              <div className="flex items-center gap-2 pt-2">
                <button
                  onClick={() => saveEdit(task.id)}
                  className="inline-flex items-center gap-2 px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-sm hover:shadow-md transform hover:scale-105 transition-all duration-200"
                  aria-label="Save changes"
                >
                  <Save className="h-4 w-4" aria-hidden="true" />
                  <span>Save</span>
                </button>
                <button
                  onClick={cancelEdit}
                  className="inline-flex items-center gap-2 px-4 py-2 border-2 border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transform hover:scale-105 transition-all duration-200"
                  aria-label="Cancel editing"
                >
                  <X className="h-4 w-4" aria-hidden="true" />
                  <span>Cancel</span>
                </button>
                <div className="ml-auto text-xs text-gray-500">
                  Press <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded">Enter</kbd> to save, <kbd className="px-1.5 py-0.5 bg-gray-100 border border-gray-300 rounded">Esc</kbd> to cancel
                </div>
              </div>
            </div>
          ) : (
            // Normal view with enhanced design
            <div className="p-5">
              <div className="flex items-start gap-4">
                {/* Custom checkbox with animation */}
                <button
                  onClick={() => onToggleComplete(task.id)}
                  className="flex-shrink-0 mt-0.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 rounded-full transition-transform hover:scale-110"
                  aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
                  aria-pressed={task.completed}
                >
                  {task.completed ? (
                    <CheckCircle2 className="h-6 w-6 text-green-500 transition-all duration-200" aria-hidden="true" />
                  ) : (
                    <Circle className="h-6 w-6 text-gray-400 hover:text-indigo-500 transition-colors duration-200" aria-hidden="true" />
                  )}
                </button>

                {/* Task content */}
                <div className="flex-1 min-w-0">
                  <h3
                    className={`text-base font-semibold transition-all duration-200 ${
                      task.completed
                        ? 'line-through text-gray-400'
                        : 'text-gray-900'
                    }`}
                  >
                    {task.title}
                  </h3>
                  {task.description && (
                    <p
                      className={`mt-1 text-sm transition-all duration-200 ${
                        task.completed ? 'text-gray-400' : 'text-gray-600'
                      }`}
                    >
                      {task.description}
                    </p>
                  )}

                  {/* Status badge */}
                  {task.completed && (
                    <span className="inline-flex items-center gap-1 mt-2 px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 animate-in fade-in zoom-in-95">
                      <CheckCircle2 className="h-3 w-3" aria-hidden="true" />
                      Completed
                    </span>
                  )}
                </div>

                {/* Action buttons */}
                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  <button
                    onClick={() => startEditing(task)}
                    className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200 hover:scale-110"
                    aria-label="Edit task"
                  >
                    <Edit2 className="h-4 w-4" aria-hidden="true" />
                  </button>
                  <button
                    onClick={() => onDelete(task.id)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-all duration-200 hover:scale-110"
                    aria-label="Delete task"
                  >
                    <Trash2 className="h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}