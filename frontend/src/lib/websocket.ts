import { io, Socket } from 'socket.io-client'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

class WebSocketManager {
  private chatSocket: Socket | null = null
  private monitoringSocket: Socket | null = null

  connectChat(onMessage: (data: any) => void) {
    if (this.chatSocket?.connected) return

    this.chatSocket = io(`${WS_URL}/ws/chat`, {
      transports: ['websocket'],
    })

    this.chatSocket.on('connect', () => {
      console.log('Chat WebSocket connected')
    })

    this.chatSocket.on('message', onMessage)

    this.chatSocket.on('disconnect', () => {
      console.log('Chat WebSocket disconnected')
    })
  }

  connectMonitoring(onMessage: (data: any) => void) {
    if (this.monitoringSocket?.connected) return

    this.monitoringSocket = io(`${WS_URL}/ws/monitoring`, {
      transports: ['websocket'],
    })

    this.monitoringSocket.on('connect', () => {
      console.log('Monitoring WebSocket connected')
    })

    this.monitoringSocket.on('message', onMessage)

    this.monitoringSocket.on('disconnect', () => {
      console.log('Monitoring WebSocket disconnected')
    })
  }

  sendChatMessage(message: string, userId?: string, context?: any) {
    if (this.chatSocket?.connected) {
      this.chatSocket.emit('message', { message, user_id: userId, context })
    }
  }

  disconnectChat() {
    if (this.chatSocket) {
      this.chatSocket.disconnect()
      this.chatSocket = null
    }
  }

  disconnectMonitoring() {
    if (this.monitoringSocket) {
      this.monitoringSocket.disconnect()
      this.monitoringSocket = null
    }
  }

  disconnectAll() {
    this.disconnectChat()
    this.disconnectMonitoring()
  }
}

export const wsManager = new WebSocketManager()
