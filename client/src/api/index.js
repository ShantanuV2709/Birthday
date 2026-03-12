import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  login: (credentials) => api.post('/auth/login', credentials),
};

export const guestApi = {
  list: () => api.get('/guests'),
};

export const expenditureApi = {
  getStats: () => api.get('/expenditure'),
};

export default api;
