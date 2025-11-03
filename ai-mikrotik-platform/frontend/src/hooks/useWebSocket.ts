import { useEffect, useRef, useState, useCallback } from 'react'
import io, { Socket } from 'socket.io-client'

interface WebSocketMessage {
  type: string
  data?: any
  message?: string
  timestamp?: string
}

interface UseWebSocketReturn {
  socket: Socket | null
  isConnected: boolean
  messages: WebSocketMessage[]
  sendMessage: (message: WebSocketMessage) => void
  connect: () => void
  disconnect: () => void
}

export const useWebSocket = (): UseWebSocketReturn => {
  const [isConnected, setIsConnected] = useState(false)
  const [messages, setMessages] = useState<WebSocketMessage[]>([])
  const socketRef = useRef<Socket | null>(null)

  const connect = useCallback(() => {
    if (socketRef.current?.connected) {
      console.log('✅ WebSocket already connected')
      return
    }

    console.log('🔌 Connecting to WebSocket...')
    
    const socket = io(import.meta.env.VITE_WS_URL || 'ws://localhost:8000', {
      path: '/ws',
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    })

    socket.on('connect', () => {
      console.log('✅ WebSocket connected')
      setIsConnected(true)
    })

    socket.on('disconnect', () => {
      console.log('❌ WebSocket disconnected')
      setIsConnected(false)
    })

    socket.on('connect_error', (error) => {
      console.error('❌ WebSocket connection error:', error)
      setIsConnected(false)
    })

    // استقبال رسالة ترحيب
    socket.on('welcome', (data: WebSocketMessage) => {
      console.log('👋 Welcome message:', data)
      setMessages(prev => [...prev, data])
    })

    // استقبال تحديثات المقاييس
    socket.on('metrics_update', (data: WebSocketMessage) => {
      console.log('📊 Metrics update:', data)
      setMessages(prev => [...prev, data])
    })

    // استقبال التنبيهات
    socket.on('alert', (data: WebSocketMessage) => {
      console.log('🚨 Alert:', data)
      setMessages(prev => [...prev, data])
    })

    // استقبال استجابة المحادثة
    socket.on('chat_response', (data: WebSocketMessage) => {
      console.log('💬 Chat response:', data)
      setMessages(prev => [...prev, data])
    })

    // استقبال تحديثات الحالة
    socket.on('status_update', (data: WebSocketMessage) => {
      console.log('📈 Status update:', data)
      setMessages(prev => [...prev, data])
    })

    socketRef.current = socket
  }, [])

  const disconnect = useCallback(() => {
    if (socketRef.current) {
      console.log('👋 Disconnecting WebSocket...')
      socketRef.current.disconnect()
      socketRef.current = null
      setIsConnected(false)
    }
  }, [])

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (socketRef.current?.connected) {
      console.log('📤 Sending message:', message)
      socketRef.current.emit(message.type, message)
    } else {
      console.error('❌ Cannot send message: WebSocket not connected')
    }
  }, [])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [disconnect])

  // Ping every 30 seconds to keep connection alive
  useEffect(() => {
    if (!isConnected) return

    const interval = setInterval(() => {
      sendMessage({ type: 'ping' })
    }, 30000)

    return () => clearInterval(interval)
  }, [isConnected, sendMessage])

  return {
    socket: socketRef.current,
    isConnected,
    messages,
    sendMessage,
    connect,
    disconnect,
  }
}
