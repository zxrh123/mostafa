import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  MessageCircle, 
  X, 
  Send, 
  Loader2,
  Sparkles,
  Brain,
  Terminal
} from 'lucide-react'
import { api } from '../services/api'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface Message {
  id: string
  role: 'user' | 'ai'
  content: string
  timestamp: Date
  decision?: any
}

const AIChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'ai',
      content: 'مرحباً! أنا العقل الصناعي المركزي للنظام. كيف يمكنني مساعدتك في إدارة شبكة MikroTik؟ 🧠',
      timestamp: new Date()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await api.chatWithAI({
        message: input,
        user_role: 'technician'
      })

      if (response.success) {
        const decision = response.decision
        
        // بناء رسالة الذكاء الصناعي
        let aiContent = `### 🎯 فهمت طلبك\n\n`
        aiContent += `**النية المكتشفة:** ${decision.intent}\n`
        aiContent += `**مستوى الثقة:** ${(decision.confidence * 100).toFixed(1)}%\n`
        aiContent += `**مستوى المخاطر:** ${decision.risk_level}\n\n`
        
        aiContent += `### 📋 خطة العمل:\n\n`
        decision.action_plan.forEach((step: string, index: number) => {
          aiContent += `${index + 1}. ${step}\n`
        })
        
        if (decision.mikrotik_script) {
          aiContent += `\n### 📜 سكربت MikroTik:\n\n`
          aiContent += `\`\`\`routeros\n${decision.mikrotik_script}\n\`\`\`\n\n`
        }
        
        aiContent += `\n### 💭 التفكير المنطقي:\n\n${decision.reasoning}\n\n`
        
        if (decision.requires_approval) {
          aiContent += `\n⚠️ **يتطلب موافقة قبل التنفيذ**\n`
        }
        
        aiContent += `\n📊 تم التحليل بواسطة: ${decision.model_used}`

        const aiMessage: Message = {
          id: Date.now().toString(),
          role: 'ai',
          content: aiContent,
          timestamp: new Date(),
          decision: decision
        }

        setMessages(prev => [...prev, aiMessage])
      }
    } catch (error) {
      console.error('Error chatting with AI:', error)
      
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'ai',
        content: '❌ عذراً، حدث خطأ في معالجة طلبك. يرجى المحاولة مرة أخرى.',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      {/* Chat Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-6 right-6 z-50 btn-accent w-16 h-16 rounded-full flex items-center justify-center shadow-glow-lg hover:shadow-glow-lg group"
          >
            <MessageCircle className="w-7 h-7 group-hover:scale-110 transition-transform" />
            <span className="absolute top-0 right-0 w-4 h-4 bg-red-500 rounded-full animate-pulse" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            className="fixed bottom-6 right-6 z-50 w-[450px] h-[650px] glass-dark rounded-3xl shadow-glow-lg overflow-hidden flex flex-col"
          >
            {/* Header */}
            <div className="gradient-bg p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <Brain className="w-8 h-8 text-white" />
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse" />
                </div>
                <div>
                  <h3 className="text-white font-bold text-lg">العقل الصناعي</h3>
                  <p className="text-white/80 text-xs">متصل • جاهز للمساعدة</p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="text-white/80 hover:text-white transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map(message => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`chat-message ${message.role}`}
                >
                  <div className={`chat-bubble ${message.role}`}>
                    {message.role === 'ai' && (
                      <div className="flex items-center gap-2 mb-2">
                        <Sparkles className="w-4 h-4 text-primary-400" />
                        <span className="text-xs font-semibold text-primary-400">
                          الذكاء الصناعي
                        </span>
                      </div>
                    )}
                    <div className="prose prose-sm prose-invert max-w-none">
                      <ReactMarkdown
                        components={{
                          code({node, inline, className, children, ...props}) {
                            const match = /language-(\w+)/.exec(className || '')
                            return !inline && match ? (
                              <SyntaxHighlighter
                                style={vscDarkPlus}
                                language={match[1]}
                                PreTag="div"
                                {...props}
                              >
                                {String(children).replace(/\n$/, '')}
                              </SyntaxHighlighter>
                            ) : (
                              <code className={className} {...props}>
                                {children}
                              </code>
                            )
                          }
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                    <div className="text-xs opacity-50 mt-2">
                      {message.timestamp.toLocaleTimeString('ar-SA')}
                    </div>
                  </div>
                </motion.div>
              ))}
              
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="chat-message ai"
                >
                  <div className="chat-bubble ai flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>جاري التفكير...</span>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-4 border-t border-white/10">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="اكتب رسالتك هنا..."
                  className="input flex-1 text-sm"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="btn-primary px-4 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <Send className="w-5 h-5" />
                  )}
                </button>
              </div>
              <p className="text-xs text-dark-500 mt-2 flex items-center gap-1">
                <Terminal className="w-3 h-3" />
                مدعوم بـ GPT-5 و Google Gemini
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

export default AIChatWidget
