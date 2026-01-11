'use client';

import { useState, useEffect } from 'react';
import { Task } from '../types';
import { Plus, Edit3, X, Sparkles } from 'lucide-react';

interface TaskFormProps {
  onCreate: (title: string, description: string) => void;
  onUpdate?: (id: number, title: string, description: string) => void;
  editingTask?: Task | null;
  onCancelEdit?: () => void;
}

const MAX_TITLE_LENGTH = 100;
const MAX_DESCRIPTION_LENGTH = 500;

export default function TaskForm({ onCreate, onUpdate, editingTask, onCancelEdit }: TaskFormProps) {
  const [title, setTitle] = useState(editingTask?.title || '');
  const [description, setDescription] = useState(editingTask?.description || '');
  const [titleError, setTitleError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Sync with editingTask prop changes
  useEffect(() => {
    if (editingTask) {
      setTitle(editingTask.title);
      setDescription(editingTask.description || '');
    }
  }, [editingTask]);

  const validateTitle = (value: string): boolean => {
    if (!value.trim()) {
      setTitleError('Task title is required');
      return false;
    }
    if (value.length > MAX_TITLE_LENGTH) {
      setTitleError(`Title must be ${MAX_TITLE_LENGTH} characters or less`);
      return false;
    }
    setTitleError('');
    return true;
  };

  const handleTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setTitle(value);
    if (titleError) validateTitle(value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateTitle(title)) return;

    setIsSubmitting(true);

    try {
      if (editingTask && onUpdate) {
        await onUpdate(editingTask.id, title.trim(), description.trim());
      } else {
        await onCreate(title.trim(), description.trim());
      }
      resetForm();
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setTitleError('');
    if (onCancelEdit) {
      onCancelEdit();
    }
  };

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape' && onCancelEdit) {
      onCancelEdit();
    }
  };

  const isEditing = !!editingTask;
  const titleCharsRemaining = MAX_TITLE_LENGTH - title.length;
  const descriptionCharsRemaining = MAX_DESCRIPTION_LENGTH - description.length;

  return (
    <form
      onSubmit={handleSubmit}
      onKeyDown={handleKeyDown}
      className="mb-8 animate-in fade-in slide-in-from-top-4 duration-300"
    >
      <div className="bg-white rounded-2xl shadow-lg border-2 border-gray-200 overflow-hidden hover:shadow-xl transition-shadow duration-300">
        {/* Header with gradient */}
        <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 px-6 py-4">
          <div className="flex items-center gap-2 text-white">
            {isEditing ? (
              <>
                <Edit3 className="h-5 w-5" aria-hidden="true" />
                <h2 className="text-lg font-semibold">Edit Task</h2>
              </>
            ) : (
              <>
                <Sparkles className="h-5 w-5" aria-hidden="true" />
                <h2 className="text-lg font-semibold">Create New Task</h2>
              </>
            )}
          </div>
        </div>

        {/* Form content */}
        <div className="px-6 py-6 space-y-5">
          {/* Title input */}
          <div>
            <label
              htmlFor="task-title"
              className="flex items-center justify-between text-sm font-medium text-gray-700 mb-2"
            >
              <span>
                Task Title <span className="text-red-500">*</span>
              </span>
              <span
                className={`text-xs ${
                  titleCharsRemaining < 20 ? 'text-orange-500 font-semibold' : 'text-gray-500'
                }`}
              >
                {titleCharsRemaining} characters left
              </span>
            </label>
            <div className="relative">
              <input
                type="text"
                id="task-title"
                value={title}
                onChange={handleTitleChange}
                onBlur={() => validateTitle(title)}
                maxLength={MAX_TITLE_LENGTH}
                className={`w-full px-4 py-3 text-base text-gray-900 placeholder-gray-400 border-2 rounded-xl shadow-sm focus:outline-none focus:ring-2 transition-all ${
                  titleError
                    ? 'border-red-300 focus:border-red-500 focus:ring-red-500'
                    : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
                }`}
                placeholder="What needs to be done?"
                aria-invalid={!!titleError}
                aria-describedby={titleError ? 'title-error' : undefined}
                autoFocus={!isEditing}
              />
              {title && !titleError && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
            {titleError && (
              <p id="title-error" className="mt-2 text-sm text-red-600 flex items-center gap-1 animate-in fade-in slide-in-from-top-1">
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                {titleError}
              </p>
            )}
          </div>

          {/* Description textarea */}
          <div>
            <label
              htmlFor="task-description"
              className="flex items-center justify-between text-sm font-medium text-gray-700 mb-2"
            >
              <span>Description (Optional)</span>
              <span
                className={`text-xs ${
                  descriptionCharsRemaining < 50 ? 'text-orange-500 font-semibold' : 'text-gray-500'
                }`}
              >
                {descriptionCharsRemaining} characters left
              </span>
            </label>
            <textarea
              id="task-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              maxLength={MAX_DESCRIPTION_LENGTH}
              rows={4}
              className="w-full px-4 py-3 text-sm text-gray-900 placeholder-gray-400 border-2 border-gray-300 rounded-xl shadow-sm focus:outline-none focus:ring-2 focus:border-indigo-500 focus:ring-indigo-500 transition-all resize-none"
              placeholder="Add more details about your task..."
            />
          </div>
        </div>

        {/* Action buttons */}
        <div className="px-6 py-4 bg-gray-50 flex items-center justify-end gap-3">
          {isEditing && onCancelEdit && (
            <button
              type="button"
              onClick={onCancelEdit}
              className="inline-flex items-center gap-2 px-5 py-2.5 border-2 border-gray-300 text-sm font-medium rounded-xl text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transform hover:scale-105 transition-all duration-200"
              aria-label="Cancel editing"
            >
              <X className="h-4 w-4" aria-hidden="true" />
              <span>Cancel</span>
            </button>
          )}
          <button
            type="submit"
            disabled={isSubmitting || !!titleError}
            className="inline-flex items-center gap-2 px-6 py-2.5 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            aria-label={isEditing ? 'Update task' : 'Create task'}
          >
            {isSubmitting ? (
              <>
                <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24" aria-hidden="true">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                <span>{isEditing ? 'Updating...' : 'Creating...'}</span>
              </>
            ) : (
              <>
                {isEditing ? (
                  <Edit3 className="h-4 w-4" aria-hidden="true" />
                ) : (
                  <Plus className="h-4 w-4" aria-hidden="true" />
                )}
                <span>{isEditing ? 'Update Task' : 'Create Task'}</span>
              </>
            )}
          </button>
        </div>

        {/* Keyboard shortcuts hint */}
        {isEditing && (
          <div className="px-6 py-2 bg-blue-50 border-t border-blue-100 text-xs text-blue-700">
            Press <kbd className="px-1.5 py-0.5 bg-white border border-blue-200 rounded">Esc</kbd> to cancel editing
          </div>
        )}
      </div>
    </form>
  );
}