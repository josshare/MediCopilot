'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { QueryResponse, Source } from '@/types/api';
import { 
  Copy, 
  Check, 
  ChevronDown, 
  ChevronUp, 
  FileText, 
  ExternalLink,
  Clock,
  Star
} from 'lucide-react';

interface ResponseDisplayProps {
  response: QueryResponse | null;
  isLoading: boolean;
}

export function ResponseDisplay({ response, isLoading }: ResponseDisplayProps) {
  const [copiedText, setCopiedText] = useState<string | null>(null);
  const [expandedSources, setExpandedSources] = useState<Set<number>>(new Set());

  const copyToClipboard = async (text: string, type: 'answer' | 'source') => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedText(type);
      setTimeout(() => setCopiedText(null), 2000);
    } catch (error) {
      console.error('Failed to copy text:', error);
    }
  };

  const toggleSourceExpansion = (index: number) => {
    const newExpanded = new Set(expandedSources);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSources(newExpanded);
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const getRelevanceColor = (score: number) => {
    if (score >= 0.8) return 'bg-green-100 text-green-800';
    if (score >= 0.6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getRelevanceLabel = (score: number) => {
    if (score >= 0.8) return 'High';
    if (score >= 0.6) return 'Medium';
    return 'Low';
  };

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="space-y-4">
            <div className="flex items-center gap-2">
              <div className="h-4 w-4 bg-blue-200 rounded animate-pulse" />
              <div className="h-4 w-32 bg-gray-200 rounded animate-pulse" />
            </div>
            <div className="space-y-2">
              <div className="h-4 w-full bg-gray-200 rounded animate-pulse" />
              <div className="h-4 w-3/4 bg-gray-200 rounded animate-pulse" />
              <div className="h-4 w-1/2 bg-gray-200 rounded animate-pulse" />
            </div>
            <div className="space-y-2">
              <div className="h-4 w-full bg-gray-200 rounded animate-pulse" />
              <div className="h-4 w-2/3 bg-gray-200 rounded animate-pulse" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!response) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-gray-500">
          <FileText className="h-12 w-12 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium">No response yet</p>
          <p className="text-sm">Ask a medical question to get started</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Main Answer */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="text-lg font-semibold text-gray-800 mb-2">
                Answer
              </CardTitle>
              <div className="flex items-center gap-2 text-sm text-gray-500">
                <Clock className="h-4 w-4" />
                <span>{formatTimestamp(response.timestamp)}</span>
                <Badge variant="outline" className="text-xs">
                  {response.sources.length} sources
                </Badge>
              </div>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(response.answer, 'answer')}
              className="flex items-center gap-2"
            >
              {copiedText === 'answer' ? (
                <Check className="h-4 w-4 text-green-600" />
              ) : (
                <Copy className="h-4 w-4" />
              )}
              {copiedText === 'answer' ? 'Copied!' : 'Copy'}
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="prose prose-sm max-w-none">
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {response.answer}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Sources */}
      {response.sources && response.sources.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-gray-800">
              Sources ({response.sources.length})
            </CardTitle>
            <p className="text-sm text-gray-500">
              References used to generate this answer
            </p>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {response.sources.map((source: Source, index: number) => (
                <div
                  key={`${source.document_id}-${source.chunk_index}`}
                  className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <FileText className="h-4 w-4 text-blue-500" />
                      <span className="font-medium text-gray-900">
                        {source.filename}
                      </span>
                      <Badge 
                        variant="secondary" 
                        className={`text-xs ${getRelevanceColor(source.relevance_score)}`}
                      >
                        <Star className="h-3 w-3 mr-1" />
                        {getRelevanceLabel(source.relevance_score)} ({Math.round(source.relevance_score * 100)}%)
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(source.content_preview, 'source')}
                        className="text-xs"
                      >
                        {copiedText === 'source' ? (
                          <Check className="h-3 w-3 text-green-600" />
                        ) : (
                          <Copy className="h-3 w-3" />
                        )}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => toggleSourceExpansion(index)}
                        className="text-xs"
                      >
                        {expandedSources.has(index) ? (
                          <ChevronUp className="h-3 w-3" />
                        ) : (
                          <ChevronDown className="h-3 w-3" />
                        )}
                      </Button>
                    </div>
                  </div>
                  
                  <div className="text-sm text-gray-600">
                    <p className="line-clamp-2">
                      {source.content_preview}
                    </p>
                  </div>

                  {expandedSources.has(index) && (
                    <div className="mt-3 p-3 bg-gray-50 rounded border-l-4 border-blue-500">
                      <div className="text-sm text-gray-700">
                        <p className="font-medium mb-1">Full Content:</p>
                        <p className="whitespace-pre-wrap leading-relaxed">
                          {source.content_preview}
                        </p>
                      </div>
                      <div className="mt-2 text-xs text-gray-500">
                        <p>Document ID: {source.document_id}</p>
                        <p>Chunk Index: {source.chunk_index}</p>
                        <p>Relevance Score: {source.relevance_score.toFixed(3)}</p>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
