import { Routes, Route } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import Dashboard from './pages/Dashboard'
import { useWebSocket } from './hooks/useWebSocket'
import { useEffect, useState } from 'react'

function App() {
  const [isConnected, setIsConnected] = useState(false)
  const { connect, disconnect, isConnected: wsConnected } = useWebSocket()

  useEffect(() => {
    // الاتصال بـ WebSocket عند تحميل التطبيق
    connect()
    setIsConnected(true)

    return () => {
      disconnect()
    }
  }, [])

  return (
    <div className="min-h-screen bg-dark-50 relative overflow-hidden">
      {/* Grid Background Pattern */}
      <div className="fixed inset-0 grid-pattern opacity-30 pointer-events-none" />
      
      {/* Gradient Orbs */}
      <div className="fixed top-0 left-0 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-pulse" />
      <div className="fixed bottom-0 right-0 w-96 h-96 bg-accent-pink/20 rounded-full blur-3xl animate-pulse delay-1000" />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-accent-cyan/20 rounded-full blur-3xl animate-pulse delay-2000" />
      
      {/* Connection Status Indicator */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="fixed top-4 left-4 z-50 glass px-4 py-2 rounded-full flex items-center gap-2"
      >
        <div className={`status-dot ${wsConnected ? 'status-healthy' : 'status-critical'}`} />
        <span className="text-sm font-semibold">
          {wsConnected ? 'متصل' : 'غير متصل'}
        </span>
      </motion.div>

      {/* Main Content */}
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </AnimatePresence>
    </div>
  )
}

export default App
