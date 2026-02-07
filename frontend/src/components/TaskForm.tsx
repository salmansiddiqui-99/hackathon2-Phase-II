'use client';

import { useState, useEffect } from 'react';
import { Task } from '../types';
import { Plus, Edit3, X, Sparkles } from 'lucide-react';
import GlassCard from './GlassCard';
import GlassInput from './GlassInput';
import GlassButton from './GlassButton';

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
      <GlassCard className="overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-500/30 via-purple-500/30 to-pink-500/30 px-6 py-4 border-b border-white/20 backdrop-blur-sm">
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
        <div className="p-6 space-y-5">
          {/* Title input */}
          <div>
            <label
              htmlFor="task-title"
              className="flex items-center justify-between text-sm font-medium text-gray-300 mb-2"
            >
              <span>
                Task Title <span className="text-red-400">*</span>
              </span>
              <span
                className={`text-xs ${
                  titleCharsRemaining < 20 ? 'text-orange-400 font-semibold' : 'text-gray-400'
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
                className={`w-full px-4 py-3 text-base text-white placeholder-gray-400 border rounded-xl bg-white/10 backdrop-blur-sm focus:outline-none focus:ring-2 transition-all ${
                  titleError
                    ? 'border-red-500/50 focus:ring-red-500 focus:border-transparent'
                    : 'border-white/20 focus:ring-blue-500 focus:border-transparent'
                }`}
                placeholder="What needs to be done?"
                aria-invalid={!!titleError}
                aria-describedby={titleError ? 'title-error' : undefined}
                autoFocus={!isEditing}
              />
              {title && !titleError && (
                <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-400">
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
            {titleError && (
              <p id="title-error" className="mt-2 text-sm text-red-400 flex items-center gap-1 animate-in fade-in slide-in-from-top-1">
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
              className="flex items-center justify-between text-sm font-medium text-gray-300 mb-2"
            >
              <span>Description (Optional)</span>
              <span
                className={`text-xs ${
                  descriptionCharsRemaining < 50 ? 'text-orange-400 font-semibold' : 'text-gray-400'
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
              className="w-full px-4 py-3 text-sm text-white placeholder-gray-400 border border-white/20 rounded-xl bg-white/10 backdrop-blur-sm focus:outline-none focus:ring-2 focus:border-transparent focus:ring-blue-500 transition-all resize-none"
              placeholder="Add more details about your task..."
            />
          </div>
        </div>

        {/* Action buttons */}
        <div className="px-6 py-4 bg-white/5 flex items-center justify-end gap-3 border-t border-white/20">
          {isEditing && onCancelEdit && (
            <GlassButton
              type="button"
              onClick={onCancelEdit}
              variant="ghost"
              size="sm"
            >
              <X className="h-4 w-4" aria-hidden="true" />
              <span>Cancel</span>
            </GlassButton>
          )}
          <GlassButton
            type="submit"
            disabled={isSubmitting || !!titleError}
            loading={isSubmitting}
            variant="primary"
            size="sm"
            icon={isEditing ? <Edit3 className="h-4 w-4" aria-hidden="true" /> : <Plus className="h-4 w-4" aria-hidden="true" />}
          >
            {isEditing ? 'Update Task' : 'Create Task'}
          </GlassButton>
        </div>

        {/* Keyboard shortcuts hint */}
        {isEditing && (
          <div className="px-6 py-2 bg-blue-500/10 border-t border-blue-500/20 text-xs text-blue-300 backdrop-blur-sm">
            Press <kbd className="px-1.5 py-0.5 bg-white/10 border border-blue-400/30 rounded">Esc</kbd> to cancel editing
          </div>
        )}
      </GlassCard>
    </form>
  );
}