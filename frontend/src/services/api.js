import axios from 'axios';

// Get API URL from environment variable or use default
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor - runs before every request
api.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed in future
    // config.headers.Authorization = `Bearer ${token}`;
    
    console.log(`Making ${config.method.toUpperCase()} request to: ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor - runs after every response
api.interceptors.response.use(
  (response) => {
    // Any status code within the range of 2xx
    console.log('Response received:', response.status);
    return response;
  },
  (error) => {
    // Any status codes outside the range of 2xx
    if (error.response) {
      // Server responded with error status
      console.error('Response error:', error.response.status, error.response.data);
      
      // Handle specific error codes
      switch (error.response.status) {
        case 404:
          console.error('Resource not found');
          break;
        case 500:
          console.error('Server error');
          break;
        default:
          console.error('An error occurred');
      }
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network error - No response from server');
      console.error('Make sure backend is running on:', API_BASE_URL);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// API helper functions (optional - for better code organization)
export const familyAPI = {
  getAll: () => api.get('/families'),
  getById: (id) => api.get(`/families/${id}`),
  create: (data) => api.post('/families', data),
  update: (id, data) => api.put(`/families/${id}`, data),
  delete: (id) => api.delete(`/families/${id}`),
};

export const personAPI = {
  create: (data) => api.post('/persons', data),
  update: (id, data) => api.put(`/persons/${id}`, data),
  delete: (id) => api.delete(`/persons/${id}`),
};

export const statsAPI = {
  get: () => api.get('/stats'),
};

export const exportAPI = {
  excel: () => api.get('/export/excel', { responseType: 'blob' }),
  csv: () => api.get('/export/csv', { responseType: 'blob' }),
};

export const searchAPI = {
  search: (query) => api.get('/search', { params: { q: query } }),
};

export default api;
