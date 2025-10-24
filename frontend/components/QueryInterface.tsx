'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { apiClient, handleApiError } from '@/lib/api';
import { QueryRequest, QueryResponse, QueryHistory } from '@/types/api';
import { Send, Loader2, History, Trash2 } from 'lucide-react';

const querySchema = z.object({
  question: z.string().min(1, 'Please enter a question').max(1000, 'Question too long'),
  max_results: z.number().min(1).max(10).optional(),
});

type QueryFormData = z.infer<typeof querySchema>;

interface QueryInterfaceProps {
  onQueryResult: (result: QueryResponse) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export function QueryInterface({ onQueryResult, isLoading, setIsLoading }: QueryInterfaceProps) {
  const [queryHistory, setQueryHistory] = useState<QueryHistory[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
  } = useForm<QueryFormData>({
    resolver: zodResolver(querySchema),
    defaultValues: {
      question: '',
      max_results: 5,
    },
  });

  const questionValue = watch('question');
  const characterCount = questionValue?.length || 0;

  const onSubmit = async (data: QueryFormData) => {
    try {
      setIsLoading(true);
      const request: QueryRequest = {
        question: data.question.trim(),
        max_results: data.max_results || 5,
      };

      const result = await apiClient.queryDocuments(request);
      
      // Add to history
      const historyItem: QueryHistory = {
        id: Date.now().toString(),
        question: request.question,
        answer: result.answer,
        timestamp: new Date().toISOString(),
        sources: result.sources,
      };
      
      setQueryHistory(prev => [historyItem, ...prev.slice(0, 9)]); // Keep last 10
      onQueryResult(result);
      reset();
    } catch (error) {
      console.error('Query failed:', error);
      // You might want to show a toast notification here
      alert(`Query failed: ${handleApiError(error)}`);
    } finally {
      setIsLoading(false);
    }
  };

  const loadHistoryItem = (item: QueryHistory) => {
    reset({ question: item.question, max_results: 5 });
    onQueryResult({
      answer: item.answer,
      sources: item.sources,
      query: item.question,
      timestamp: item.timestamp,
    });
    setShowHistory(false);
  };

  const clearHistory = () => {
    setQueryHistory([]);
  };

  return (
    <div className="space-y-4">
      {/* Query Form */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl font-semibold text-gray-800">
              Medical Query Assistant
            </CardTitle>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowHistory(!showHistory)}
                className="flex items-center gap-2"
              >
                <History className="h-4 w-4" />
                History ({queryHistory.length})
              </Button>
              {queryHistory.length > 0 && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={clearHistory}
                  className="text-red-600 hover:text-red-700"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
              <Textarea
                {...register('question')}
                placeholder="Ask a medical question... (e.g., What are the side effects of paracetamol?)"
                className="min-h-[120px] resize-none text-base"
                disabled={isLoading}
              />
              <div className="flex justify-between items-center text-sm text-gray-500">
                <span className={characterCount > 900 ? 'text-red-500' : ''}>
                  {characterCount}/1000 characters
                </span>
                {errors.question && (
                  <span className="text-red-500">{errors.question.message}</span>
                )}
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <label htmlFor="max_results" className="text-sm text-gray-600">
                  Max Results:
                </label>
                <select
                  {...register('max_results', { valueAsNumber: true })}
                  className="px-2 py-1 border rounded text-sm"
                  disabled={isLoading}
                >
                  <option value={3}>3</option>
                  <option value={5}>5</option>
                  <option value={7}>7</option>
                  <option value={10}>10</option>
                </select>
              </div>

              <Button
                type="submit"
                disabled={isLoading || !questionValue?.trim()}
                className="flex items-center gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    Ask Question
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Query History */}
      {showHistory && queryHistory.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Recent Queries</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {queryHistory.map((item) => (
                <div
                  key={item.id}
                  className="p-3 border rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                  onClick={() => loadHistoryItem(item)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {item.question}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(item.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <Badge variant="secondary" className="ml-2 text-xs">
                      {item.sources.length} sources
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
