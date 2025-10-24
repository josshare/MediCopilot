'use client';

import { useState, useCallback, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { apiClient, handleApiError } from '@/lib/api';
import { DocumentUploadResponse, UploadProgress } from '@/types/api';
import { 
  Upload, 
  FileText, 
  CheckCircle, 
  XCircle, 
  Trash2, 
  AlertCircle,
  File,
  Loader2
} from 'lucide-react';

interface DocumentUploadProps {
  onUploadSuccess?: (response: DocumentUploadResponse) => void;
}

export function DocumentUpload({ onUploadSuccess }: DocumentUploadProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploads, setUploads] = useState<UploadProgress[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedTypes = ['.pdf', '.txt', '.docx', '.doc'];
  const maxFileSize = 10 * 1024 * 1024; // 10MB

  const validateFile = (file: File): string | null => {
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(fileExt)) {
      return `File type ${fileExt} not supported. Allowed types: ${allowedTypes.join(', ')}`;
    }
    
    if (file.size > maxFileSize) {
      return `File too large. Maximum size: ${maxFileSize / (1024 * 1024)}MB`;
    }
    
    return null;
  };

  const handleFileSelect = useCallback((files: FileList | null) => {
    if (!files) return;

    Array.from(files).forEach((file) => {
      const error = validateFile(file);
      
      const uploadItem: UploadProgress = {
        file,
        progress: 0,
        status: error ? 'error' : 'uploading',
        error: error || undefined,
      };

      setUploads(prev => [...prev, uploadItem]);

      if (!error) {
        uploadFile(file, uploadItem);
      }
    });
  }, []);

  const uploadFile = async (file: File, uploadItem: UploadProgress) => {
    try {
      setIsUploading(true);
      
      const response = await apiClient.uploadDocument(file, (progress) => {
        setUploads(prev => 
          prev.map(upload => 
            upload.file === file 
              ? { ...upload, progress }
              : upload
          )
        );
      });

      setUploads(prev => 
        prev.map(upload => 
          upload.file === file 
            ? { ...upload, progress: 100, status: 'success' }
            : upload
        )
      );

      onUploadSuccess?.(response);
    } catch (error) {
      console.error('Upload failed:', error);
      setUploads(prev => 
        prev.map(upload => 
          upload.file === file 
            ? { ...upload, status: 'error', error: handleApiError(error) }
            : upload
        )
      );
    } finally {
      setIsUploading(false);
    }
  };

  const removeUpload = (file: File) => {
    setUploads(prev => prev.filter(upload => upload.file !== file));
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  }, [handleFileSelect]);

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFileSelect(e.target.files);
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  const getStatusIcon = (status: UploadProgress['status']) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'uploading':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />;
      default:
        return <File className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: UploadProgress['status']) => {
    switch (status) {
      case 'success':
        return 'bg-green-100 text-green-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      case 'uploading':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-gray-800">
            Upload Medical Documents
          </CardTitle>
          <p className="text-sm text-gray-500">
            Upload PDF, TXT, or DOCX files to add them to the knowledge base
          </p>
        </CardHeader>
        <CardContent>
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              isDragOver
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-gray-400'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <Upload className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium text-gray-700 mb-2">
              Drop files here or click to browse
            </p>
            <p className="text-sm text-gray-500 mb-4">
              Supported formats: PDF, TXT, DOCX (max 10MB each)
            </p>
            <Button onClick={openFileDialog} disabled={isUploading}>
              {isUploading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <FileText className="h-4 w-4 mr-2" />
                  Choose Files
                </>
              )}
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept={allowedTypes.join(',')}
              onChange={handleFileInputChange}
              className="hidden"
            />
          </div>
        </CardContent>
      </Card>

      {/* Upload Progress */}
      {uploads.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-gray-800">
              Upload Progress
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {uploads.map((upload, index) => (
                <div key={`${upload.file.name}-${index}`} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {getStatusIcon(upload.status)}
                      <span className="text-sm font-medium text-gray-700">
                        {upload.file.name}
                      </span>
                      <Badge 
                        variant="secondary" 
                        className={`text-xs ${getStatusColor(upload.status)}`}
                      >
                        {upload.status}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-gray-500">
                        {(upload.file.size / (1024 * 1024)).toFixed(1)} MB
                      </span>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => removeUpload(upload.file)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-3 w-3" />
                      </Button>
                    </div>
                  </div>

                  {upload.status === 'uploading' && (
                    <Progress value={upload.progress} className="h-2" />
                  )}

                  {upload.status === 'success' && (
                    <div className="text-xs text-green-600">
                      ✓ Upload completed successfully
                    </div>
                  )}

                  {upload.status === 'error' && upload.error && (
                    <div className="flex items-center gap-2 text-xs text-red-600">
                      <AlertCircle className="h-3 w-3" />
                      <span>{upload.error}</span>
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
