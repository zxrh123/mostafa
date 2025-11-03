import { useEffect, useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Bot, User, Sparkles } from 'lucide-react'
import { chatApi } from '@/lib/api'
import { wsManager } from '@/lib/websocket'

interface Message {
  id: string
  type: 'user' | 'ai'
  content: string
  timestamp: Date
  actions?: any[]
  confidence?: number
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'ai',
      content: '??????! ??? ??????? ????? ?????? ????? MikroTik. ??? ?????? ??????? ??????',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    wsManager.connectChat((data) => {
      if (data.type === 'ai_response') {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now().toString(),
            type: 'ai',
            content: data.message,
            timestamp: new Date(),
            actions: data.actions,
            confidence: data.confidence,
          },
        ])
        setIsLoading(false)
      }
    })

    return () => {
      wsManager.disconnectChat()
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      wsManager.sendChatMessage(input, 'user-1')
    } catch (error) {
      console.error('Error sending message:', error)
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)]">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-dark" />
          </div>
          <div>
            <h1 className="text-3xl font-bold glow-text text-primary">??????? ?????</h1>
            <p className="text-gray-400">???? ?? AI ?????? ?????</p>
          </div>
        </div>
      </motion.div>

      {/* Messages */}
      <div className="flex-1 glass-effect rounded-xl border border-primary/20 p-6 overflow-y-auto mb-6">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className={`flex gap-4 mb-6 ${
                message.type === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.type === 'user'
                    ? 'bg-gradient-to-br from-secondary to-primary'
                    : 'bg-gradient-to-br from-primary to-secondary'
                }`}
              >
                {message.type === 'user' ? (
                  <User className="w-5 h-5 text-dark" />
                ) : (
                  <Bot className="w-5 h-5 text-dark" />
                )}
              </div>
              <div
                className={`flex-1 ${
                  message.type === 'user' ? 'text-left' : 'text-right'
                }`}
              >
                <div
                  className={`inline-block p-4 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-primary/20 text-right'
                      : 'bg-dark-lighter text-right'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  {message.confidence && (
                    <p className="text-xs text-gray-400 mt-2">
                      ?????: {(message.confidence * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
                {message.actions && message.actions.length > 0 && (
                  <div className="mt-2 space-y-2">
                    {message.actions.map((action, idx) => (
                      <button
                        key={idx}
                        className="px-4 py-2 bg-primary/20 rounded-lg text-sm hover:bg-primary/30 transition-colors"
                      >
                        ?????: {action.type}
                      </button>
                    ))}
                  </div>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  {message.timestamp.toLocaleTimeString('ar-EG')}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex gap-4"
          >
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
              <Bot className="w-5 h-5 text-dark" />
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex gap-4"
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="???? ?????? ???..."
          className="flex-1 px-6 py-4 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
          disabled={isLoading}
        />
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          className="px-6 py-4 bg-gradient-to-r from-primary to-secondary rounded-lg font-medium hover:shadow-lg hover:shadow-primary/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Send className="w-5 h-5" />
        </motion.button>
      </motion.div>
    </div>
  )
}
