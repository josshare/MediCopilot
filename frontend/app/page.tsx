'use client';

import { useState } from 'react';
import { QueryInterface } from '@/components/QueryInterface';
import { ResponseDisplay } from '@/components/ResponseDisplay';
import { DocumentUpload } from '@/components/DocumentUpload';
import { HealthStatus } from '@/components/HealthStatus';
import { QueryResponse, DocumentUploadResponse } from '@/types/api';
import { Brain, FileText, MessageSquare, Upload } from 'lucide-react';
import { toast } from 'sonner';

export default function Home() {
  const [queryResponse, setQueryResponse] = useState<QueryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'query' | 'upload'>('query');

  const handleQueryResult = (result: QueryResponse) => {
    setQueryResponse(result);
    toast.success('Query processed successfully!');
  };

  const handleUploadSuccess = (response: DocumentUploadResponse) => {
    toast.success(`Document "${response.filename}" uploaded successfully!`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">MediCopilot</h1>
                <p className="text-sm text-gray-500">Medical AI Assistant</p>
              </div>
            </div>
            <HealthStatus />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Tab Navigation */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('query')}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                  activeTab === 'query'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <MessageSquare className="h-4 w-4" />
                Ask Questions
              </button>
              <button
                onClick={() => setActiveTab('upload')}
                className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                  activeTab === 'upload'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <Upload className="h-4 w-4" />
                Upload Documents
              </button>
            </nav>
          </div>
        </div>

        {/* Content Area */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Query Interface */}
          <div className="space-y-6">
            <QueryInterface
              onQueryResult={handleQueryResult}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
            
            {activeTab === 'upload' && (
              <DocumentUpload onUploadSuccess={handleUploadSuccess} />
            )}
          </div>

          {/* Right Column - Response Display */}
          <div className="space-y-6">
            <ResponseDisplay
              response={queryResponse}
              isLoading={isLoading}
            />
          </div>
        </div>

        {/* Quick Start Guide */}
        {!queryResponse && !isLoading && (
          <div className="mt-12">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
                Welcome to MediCopilot
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-4">
                    <FileText className="h-6 w-6 text-blue-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Upload Documents
                  </h3>
                  <p className="text-gray-600 text-sm">
                    Upload medical documents (PDF, TXT, DOCX) to build your knowledge base
                  </p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mx-auto mb-4">
                    <MessageSquare className="h-6 w-6 text-green-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Ask Questions
                  </h3>
                  <p className="text-gray-600 text-sm">
                    Ask medical questions and get AI-powered answers based on your documents
                  </p>
                </div>
                <div className="text-center">
                  <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mx-auto mb-4">
                    <Brain className="h-6 w-6 text-purple-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Get Insights
                  </h3>
                  <p className="text-gray-600 text-sm">
                    Receive detailed answers with source citations and relevance scores
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>MediCopilot - AI-Powered Medical Assistant</p>
            <p className="mt-1">Built with Next.js, FastAPI, and Weaviate</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
