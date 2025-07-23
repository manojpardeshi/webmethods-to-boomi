// API Configuration
export const API_CONFIG = {
  baseURL: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000',
  endpoints: {
    migrate: '/migrate',
    health: '/health'
  }
};

export const getApiUrl = (endpoint: keyof typeof API_CONFIG.endpoints): string => {
  return `${API_CONFIG.baseURL}${API_CONFIG.endpoints[endpoint]}`;
};
