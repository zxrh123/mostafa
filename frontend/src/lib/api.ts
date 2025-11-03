import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Router APIs
export const routerApi = {
  list: () => api.get('/routers'),
  get: (routerId: string) => api.get(`/routers/${routerId}`),
  add: (data: any) => api.post('/routers', data),
  remove: (routerId: string) => api.delete(`/routers/${routerId}`),
}

// Monitoring APIs
export const monitoringApi = {
  status: () => api.get('/monitoring/status'),
  getRouterStatus: (routerId: string) => api.get(`/monitoring/routers/${routerId}`),
  getAllRoutersStatus: () => api.get('/monitoring/routers'),
}

// Execution APIs
export const executionApi = {
  executeScript: (data: any) => api.post('/execution/script', data),
  executeWithAI: (data: any) => api.post('/execution/ai', data),
  getHistory: (routerId: string, limit = 100) => api.get(`/execution/history/${routerId}?limit=${limit}`),
  rollback: (executionId: string, routerId: string) => api.post(`/execution/rollback/${executionId}`, { router_id: routerId }),
}

// Chat APIs
export const chatApi = {
  sendMessage: (data: any) => api.post('/chat/message', data),
  generateScript: (intent: string, parameters: any) => api.post('/chat/generate-script', { intent, parameters }),
}
