import axios from 'axios';
import { getApiUrl } from '../config/api.config';

export interface MigrationResponse {
  success: boolean;
  plan_content?: string;
  error?: string;
  filename: string;
}

export const apiService = {
  async checkHealth(): Promise<boolean> {
    try {
      const response = await axios.get(getApiUrl('health'));
      return response.data.status === 'healthy';
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  },

  async migrateFiles(files: File[]): Promise<void> {
    const formData = new FormData();
    
    // Append each file to FormData
    files.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post(getApiUrl('migrate'), formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob', // Important for file download
      });

      // Create a blob from the response
      const blob = new Blob([response.data], { type: 'text/markdown' });
      
      // Create a temporary URL for the blob
      const url = window.URL.createObjectURL(blob);
      
      // Create a temporary anchor element and trigger download
      const link = document.createElement('a');
      link.href = url;
      link.download = 'Plan.md';
      document.body.appendChild(link);
      link.click();
      
      // Clean up
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Migration failed');
      }
      throw error;
    }
  }
};
