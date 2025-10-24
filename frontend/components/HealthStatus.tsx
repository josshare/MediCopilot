'use client';

import { useState, useEffect } from 'react';
import { Badge } from '@/components/ui/badge';
import { apiClient, checkApiHealth } from '@/lib/api';
import { HealthResponse } from '@/types/api';
import { Wifi, WifiOff, Database, Brain, AlertCircle } from 'lucide-react';

interface HealthStatusProps {
  className?: string;
}

export function HealthStatus({ className = '' }: HealthStatusProps) {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkHealth = async () => {
    try {
      setIsLoading(true);
      const healthData = await apiClient.getHealth();
      setHealth(healthData);
      setLastChecked(new Date());
    } catch (error) {
      console.error('Health check failed:', error);
      setHealth(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Initial check
    checkHealth();
    
    // Set up interval for auto-refresh every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'ok':
        return 'bg-green-500';
      case 'unhealthy':
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-yellow-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
      case 'ok':
        return <Wifi className="h-3 w-3" />;
      case 'unhealthy':
      case 'error':
        return <WifiOff className="h-3 w-3" />;
      default:
        return <AlertCircle className="h-3 w-3" />;
    }
  };

  if (isLoading && !health) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <div className="h-2 w-2 rounded-full bg-gray-400 animate-pulse" />
        <span className="text-sm text-gray-500">Checking...</span>
      </div>
    );
  }

  if (!health) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <WifiOff className="h-3 w-3 text-red-500" />
        <span className="text-sm text-red-500">API Offline</span>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      {/* Overall Status */}
      <div className="flex items-center gap-1">
        {getStatusIcon(health.status)}
        <Badge 
          variant={health.status === 'healthy' ? 'default' : 'destructive'}
          className="text-xs"
        >
          {health.status === 'healthy' ? 'Online' : 'Offline'}
        </Badge>
      </div>

      {/* API Status */}
      <div className="flex items-center gap-1">
        <Database className="h-3 w-3 text-blue-500" />
        <span className="text-xs text-gray-600">
          API: {health.api_status}
        </span>
      </div>

      {/* Weaviate Status */}
      <div className="flex items-center gap-1">
        <Brain className="h-3 w-3 text-purple-500" />
        <span className="text-xs text-gray-600">
          DB: {health.weaviate_status}
        </span>
      </div>

      {/* Last Checked */}
      {lastChecked && (
        <span className="text-xs text-gray-400">
          {lastChecked.toLocaleTimeString()}
        </span>
      )}
    </div>
  );
}
