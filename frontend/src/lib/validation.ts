// Validation utilities for the Todo application

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export const validateTask = (title: string, description?: string): ValidationResult => {
  const errors: string[] = [];

  // Validate title
  if (!title || title.trim().length === 0) {
    errors.push('Title is required');
  } else if (title.trim().length > 255) {
    errors.push('Title must be less than 255 characters');
  }

  // Validate description if provided
  if (description && description.length > 1000) {
    errors.push('Description must be less than 1000 characters');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};

export const validateUser = (email: string, password: string): ValidationResult => {
  const errors: string[] = [];

  // Validate email
  if (!email || email.trim().length === 0) {
    errors.push('Email is required');
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    errors.push('Please enter a valid email address');
  }

  // Validate password
  if (!password || password.length < 6) {
    errors.push('Password must be at least 6 characters long');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};

export const validatePasswordConfirmation = (password: string, confirmPassword: string): ValidationResult => {
  const errors: string[] = [];

  if (password !== confirmPassword) {
    errors.push('Passwords do not match');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};