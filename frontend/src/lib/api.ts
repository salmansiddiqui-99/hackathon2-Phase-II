// API client utility for making authenticated requests

import { Task } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || API_BASE_URL;
  }

  private getAuthToken(): string | null {
    // In a real app, you might store the token in a more secure way
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Build the initial headers object
    const initialHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string> || {}),
    };

    // Add authorization header if token exists
    const token = this.getAuthToken();
    if (token) {
      initialHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config: RequestInit = {
      ...options,
      headers: initialHeaders,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    // Handle responses that don't have a body (like DELETE requests)
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  // Authentication endpoints
  async login(email: string, password: string) {
    return this.request<{access_token: string}>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async register(email: string, password: string) {
    return this.request<{access_token: string}>('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async logout() {
    // Logout is handled client-side by removing the token
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  // Task endpoints
  async getTasks() {
    return this.request<Task[]>('/api/tasks');
  }

  async createTask(taskData: { title: string; description?: string }) {
    return this.request<Task>('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async getTaskById(taskId: number) {
    return this.request<Task>(`/api/tasks/${taskId}`);
  }

  async updateTask(taskId: number, taskData: { title?: string; description?: string; completed?: boolean }) {
    return this.request<Task>(`/api/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId: number) {
    return this.request(`/api/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: number) {
    return this.request<Task>(`/api/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }
}

export const apiClient = new ApiClient();