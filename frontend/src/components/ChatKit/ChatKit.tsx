import { useState, useRef, useEffect } from 'react';
import Head from 'next/head';
import GlassCard from '../GlassCard';
import GlassInput from '../GlassInput';
import GlassButton from '../GlassButton';
import { Send, MessageSquare, User } from 'lucide-react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatKitProps {
  userId: number;
  apiUrl?: string;
  initialMessages?: Message[];
  onStatusChange?: (status: string) => void;
  onMessagesChange?: (messages: Message[]) => void;
}

/**
 * ChatKit Component - Custom AI Chat Component
 *
 * This component serves as an OpenAI ChatKit-like interface that connects
 * to our backend API with proper JWT authentication.
 *
 * Domain Allowlist Configuration for Production:
 * - For production deployments, ensure CORS settings allow your domain
 * - Add your production domain to the allowed origins in your backend
 * - This prevents unauthorized domains from accessing your chat endpoint
 */
export default function ChatKit({ userId, apiUrl, initialMessages = [], onStatusChange, onMessagesChange }: ChatKitProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. You can ask me to help you manage your tasks - create, update, complete, or delete tasks using natural language.',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  // Default API URL if not provided
  const defaultApiUrl = apiUrl || `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/api/chat`;

  // Handle scroll to bottom
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Simulate loading complete
  useEffect(() => {
    setIsLoading(false);
    if (onStatusChange) onStatusChange('loaded');
  }, [onStatusChange]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim()) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');

    try {
      // Call the backend chat API with JWT authentication
      const response = await fetch(defaultApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          message: inputValue.trim(),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response to chat
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);

      // Call onMessagesChange callback if provided
      if (onMessagesChange) {
        onMessagesChange([...messages, userMessage, aiMessage]);
      }
    } catch (err) {
      console.error('Error sending message:', err);

      // Add error message to chat
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  };

  if (hasError) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-red-500">Error loading Chat interface. Please try again later.</div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <GlassCard className="flex flex-col h-full overflow-hidden">
      {/* Chat header */}
      <div className="bg-gradient-to-r from-indigo-500/30 to-purple-600/30 p-4 text-white border-b border-white/20 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <MessageSquare className="h-6 w-6" />
          <h2 className="text-lg font-semibold">AI Chat Assistant</h2>
        </div>
        <p className="text-indigo-100 text-sm mt-1">Ask me to manage your tasks with natural language</p>
      </div>

      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[calc(100vh-250px)] bg-white/5 backdrop-blur-sm">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {message.role === 'assistant' && (
              <div className="flex-shrink-0 w-8 h-8 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                <MessageSquare className="h-4 w-4 text-white" />
              </div>
            )}

            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 backdrop-blur-sm ${
                message.role === 'user'
                  ? 'bg-gradient-to-r from-indigo-500/30 to-purple-600/30 text-white rounded-br-md border border-white/20'
                  : 'bg-white/20 text-gray-200 rounded-bl-md border border-white/20'
              }`}
            >
              <div className="whitespace-pre-wrap break-words">{message.content}</div>
              <div
                className={`text-xs mt-1 ${
                  message.role === 'user' ? 'text-indigo-200' : 'text-gray-400'
                }`}
              >
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>

            {message.role === 'user' && (
              <div className="flex-shrink-0 w-8 h-8 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                <User className="h-4 w-4 text-white" />
              </div>
            )}
          </div>
        ))}

        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="border-t border-white/20 p-4 bg-white/5 backdrop-blur-sm">
        <div className="flex gap-2">
          <GlassInput
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me to manage your tasks (e.g., 'Add a task to buy groceries')..."
            className="flex-1"
            variant="small"
          />
          <GlassButton
            type="submit"
            disabled={!inputValue.trim()}
            icon={<Send className="h-5 w-5" />}
            size="sm"
          >
            <span className="hidden sm:inline">Send</span>
          </GlassButton>
        </div>
        <p className="text-xs text-gray-400 mt-2 text-center">
          Ask me to create, update, complete, or delete tasks using natural language
        </p>
      </form>
    </GlassCard>
  );
}