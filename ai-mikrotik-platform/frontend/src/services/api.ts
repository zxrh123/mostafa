import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const axiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor للأخطاء
axiosInstance.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const api = {
  // Health Check
  healthCheck: async () => {
    return axiosInstance.get('/api/health')
  },

  // Get System Status
  getStatus: async () => {
    return axiosInstance.get('/api/status')
  },

  // Get Metrics
  getMetrics: async () => {
    return axiosInstance.get('/api/metrics')
  },

  // Get Alerts
  getAlerts: async () => {
    return axiosInstance.get('/api/alerts')
  },

  // Get AI Status
  getAIStatus: async () => {
    return axiosInstance.get('/api/ai/status')
  },

  // Chat with AI
  chatWithAI: async (data: { message: string; user_role: string }) => {
    return axiosInstance.post('/api/chat', data)
  },

  // Execute Script
  executeScript: async (data: {
    script: string
    dry_run: boolean
    description: string
  }) => {
    return axiosInstance.post('/api/execute', data)
  },
}

export default api
