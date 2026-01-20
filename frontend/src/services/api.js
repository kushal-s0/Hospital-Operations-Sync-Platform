import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          });

          const { access } = response.data;
          localStorage.setItem('access_token', access);

          // Retry the original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Authentication API
export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
    username,
    password,
  });
  return response.data;
};

export const logout = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  try {
    await api.post('/auth/logout/', { refresh: refreshToken });
  } catch (error) {
    console.error('Logout error:', error);
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  }
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/profile/');
  return response.data;
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

// Patients API
export const patientsAPI = {
  getAll: () => api.get('/patients/'),
  getById: (id) => api.get(`/patients/${id}/`),
  create: (data) => api.post('/patients/', data),
  update: (id, data) => api.put(`/patients/${id}/`, data),
  delete: (id) => api.delete(`/patients/${id}/`),
};

// OPD Queue API
export const opdAPI = {
  getCurrentQueue: () => api.get('/opd/queue/current_queue/'),
  getAll: () => api.get('/opd/queue/'),
  create: (data) => api.post('/opd/queue/', data),
  startConsultation: (id) => api.post(`/opd/queue/${id}/start_consultation/`),
  endConsultation: (id) => api.post(`/opd/queue/${id}/end_consultation/`),
  getStatistics: () => api.get('/opd/statistics/'),
  
  // ML Wait Time Prediction Endpoint
  predictWaitTime: (patientData) => api.post('/opd/predict-wait-time/', patientData || {}),
};

// Beds API
export const bedsAPI = {
  getAll: () => api.get('/beds/'),
  getAvailable: () => api.get('/beds/available/'),
  getOccupancySummary: () => api.get('/beds/occupancy_summary/'),
  getDepartments: () => api.get('/beds/departments/'),
  getHospitals: () => api.get('/interhospital/hospitals/'),
  create: (data) => api.post('/beds/', data),
  update: (id, data) => api.put(`/beds/${id}/`, data),
  patch: (id, data) => api.patch(`/beds/${id}/`, data),
  delete: (id) => api.delete(`/beds/${id}/`),
};

// Admissions API
export const admissionsAPI = {
  getAll: () => api.get('/admissions/'),
  getCurrent: () => api.get('/admissions/current/'),
  create: (data) => api.post('/admissions/', data),
  discharge: (id) => api.post(`/admissions/${id}/discharge/`),
  matchBed: (requirements) => api.post('/admissions/match_bed/', requirements),
};

// Inventory API
export const inventoryAPI = {
  getAll: () => api.get('/inventory/items/'),
  getItems: () => api.get('/inventory/items/'),
  getLowStock: () => api.get('/inventory/items/low_stock/'),
  getExpiringSoon: () => api.get('/inventory/items/expiring_soon/'),
  getCategories: () => api.get('/inventory/categories/'),
  createTransaction: (data) => api.post('/inventory/transactions/', data),
  
  // Stock management
  addStock: (data) => api.post('/inventory/items/', data),
  updateStock: (itemId, data) => api.patch(`/inventory/items/${itemId}/update_stock/`, data),
  
  // ML Prediction Endpoints
  getPrediction: (itemId) => api.get(`/inventory/predict/${itemId}/`),
  getAllAlerts: () => api.get('/inventory/alerts/'),
  getDemandForecast: (days = 7) => api.get(`/inventory/demand-forecast/?days=${days}`),
  getManualPrediction: (itemData) => api.post('/inventory/predict/manual/', { item_data: itemData }),
  
  // ML Predictions (alternative format)
  getMLPredictions: () => api.get('/inventory/alerts/'),
};

// Dashboard API
export const dashboardAPI = {
  getSummary: () => api.get('/dashboard/summary/'),
  getDepartmentSummary: () => api.get('/dashboard/departments/'),
};

// Inter-Hospital API
export const interHospitalAPI = {
  getHospitals: () => api.get('/interhospital/hospitals/'),
  getCityDashboard: () => api.get('/interhospital/city-dashboard/'),
  getLatestCapacity: () => api.get('/interhospital/capacity/latest/'),
};

export default api;
