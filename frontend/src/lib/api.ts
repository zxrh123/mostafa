import axios from 'axios';

export const api = axios.create({
  baseURL: '/api/v1',
  timeout: 12000
});

export interface AICommandPayload {
  conversation_id: string;
  sender: string;
  message: string;
  context?: Record<string, unknown>;
}

export const sendAICommand = async (payload: AICommandPayload) => {
  const response = await api.post('/ai/command', payload);
  return response.data;
};

export const fetchMonitoringSnapshot = async () => {
  const response = await api.get('/monitoring/snapshot');
  return response.data;
};
