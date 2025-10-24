// API Types matching the FastAPI models

export interface QueryRequest {
  question: string;
  max_results?: number;
}

export interface QueryResponse {
  answer: string;
  sources: Source[];
  query: string;
  timestamp: string;
}

export interface Source {
  filename: string;
  chunk_index: number;
  content_preview: string;
  relevance_score: number;
  document_id: string;
}

export interface DocumentUploadResponse {
  document_id: string;
  filename: string;
  chunks_created: number;
  message: string;
}

export interface HealthResponse {
  status: string;
  weaviate_status: string;
  api_status: string;
  timestamp: string;
}

export interface DocumentStats {
  total_documents: number;
  total_chunks: number;
  last_updated: string;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
  timestamp: string;
}

// UI State Types
export interface QueryHistory {
  id: string;
  question: string;
  answer: string;
  timestamp: string;
  sources: Source[];
}

export interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'success' | 'error';
  error?: string;
}
