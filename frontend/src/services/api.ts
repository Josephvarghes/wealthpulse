import { FullAnalysisResponse } from '../types';

const API_BASE = '/api';

export const api = {
  async uploadFile(file: File): Promise<FullAnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      if (errorData && errorData.detail) {
        if (typeof errorData.detail === 'object' && errorData.detail.message) {
          const detailMsg = errorData.detail.errors?.length
            ? `${errorData.detail.message}: ${errorData.detail.errors.join('; ')}`
            : errorData.detail.message;
          throw new Error(detailMsg);
        }
        throw new Error(String(errorData.detail));
      }
      throw new Error(`Upload failed with status ${response.status}`);
    }

    return response.json();
  },

  async loadDemoData(): Promise<FullAnalysisResponse> {
    const response = await fetch(`${API_BASE}/upload/demo`, {
      method: 'POST',
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Failed to load demo data (${response.status})`);
    }

    return response.json();
  },

  async checkHealth(): Promise<any> {
    const response = await fetch(`${API_BASE}/health`);
    return response.json();
  },
};

