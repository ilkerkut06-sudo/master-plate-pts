import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API methods
export const cameraAPI = {
  getAll: () => api.get('/api/cameras'),
  get: (id) => api.get(`/api/cameras/${id}`),
  create: (data) => api.post('/api/cameras', data),
  update: (id, data) => api.put(`/api/cameras/${id}`, data),
  delete: (id) => api.delete(`/api/cameras/${id}`),
  start: (id) => api.post(`/api/cameras/${id}/start`),
  stop: (id) => api.post(`/api/cameras/${id}/stop`),
  getStats: (id) => api.get(`/api/cameras/${id}/stats`),
  setEngine: (id, engine) => api.post(`/api/cameras/${id}/ocr-engine`, { engine }),
}

export const plateAPI = {
  getAll: (limit = 50) => api.get(`/api/plates?limit=${limit}`),
  get: (id) => api.get(`/api/plates/${id}`),
  getByCamera: (cameraId, limit = 50) => api.get(`/api/plates/camera/${cameraId}?limit=${limit}`),
  search: (plateNumber) => api.get(`/api/plates/search/${plateNumber}`),
  getStats: () => api.get('/api/plates/stats/summary'),
}

export const gateAPI = {
  getAll: () => api.get('/api/gates'),
  get: (id) => api.get(`/api/gates/${id}`),
  create: (data) => api.post('/api/gates', data),
  update: (id, data) => api.put(`/api/gates/${id}`, data),
  delete: (id) => api.delete(`/api/gates/${id}`),
  open: (id, duration) => api.post(`/api/gates/${id}/open`, { duration }),
  test: (id) => api.post(`/api/gates/${id}/test`),
}

export const siteAPI = {
  getAll: () => api.get('/api/sites'),
  get: (id) => api.get(`/api/sites/${id}`),
  create: (data) => api.post('/api/sites', data),
  update: (id, data) => api.put(`/api/sites/${id}`, data),
  delete: (id) => api.delete(`/api/sites/${id}`),
}

export const settingsAPI = {
  getOCREngines: () => api.get('/api/settings/ocr-engines'),
  setOCREngine: (engine) => api.post('/api/settings/ocr-engine', { engine }),
  getSystemInfo: () => api.get('/api/settings/system-info'),
}

export const logAPI = {
  getAll: (limit = 100) => api.get(`/api/logs?limit=${limit}`),
  getByType: (type, limit = 100) => api.get(`/api/logs/type/${type}?limit=${limit}`),
  getBySeverity: (severity, limit = 100) => api.get(`/api/logs/severity/${severity}?limit=${limit}`),
  clean: (days = 30) => api.delete(`/api/logs/clean?days=${days}`),
}

export default api