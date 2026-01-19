import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
};

// Beds API
export const bedsAPI = {
  getAll: () => api.get('/beds/'),
  getAvailable: () => api.get('/beds/available/'),
  getOccupancySummary: () => api.get('/beds/occupancy_summary/'),
  getDepartments: () => api.get('/beds/departments/'),
  update: (id, data) => api.put(`/beds/${id}/`, data),
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
  getItems: () => api.get('/inventory/items/'),
  getLowStock: () => api.get('/inventory/items/low_stock/'),
  getExpiringSoon: () => api.get('/inventory/items/expiring_soon/'),
  getCategories: () => api.get('/inventory/categories/'),
  createTransaction: (data) => api.post('/inventory/transactions/', data),
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
