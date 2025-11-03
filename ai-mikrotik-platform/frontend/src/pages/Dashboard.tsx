import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  Activity, 
  Cpu, 
  HardDrive, 
  Network, 
  Users, 
  Zap,
  AlertCircle,
  TrendingUp,
  Server
} from 'lucide-react'
import AIChatWidget from '../components/AIChatWidget'
import MetricsChart from '../components/MetricsChart'
import AlertPanel from '../components/AlertPanel'
import SystemStatus from '../components/SystemStatus'
import { api } from '../services/api'

const Dashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date())

  // تحديث الوقت كل ثانية
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)
    return () => clearInterval(interval)
  }, [])

  // جلب حالة النظام
  const { data: systemStatus, isLoading: statusLoading } = useQuery({
    queryKey: ['system-status'],
    queryFn: () => api.getStatus(),
    refetchInterval: 5000, // كل 5 ثواني
  })

  // جلب المقاييس
  const { data: metrics, isLoading: metricsLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: () => api.getMetrics(),
    refetchInterval: 5000,
  })

  // جلب التنبيهات
  const { data: alerts, isLoading: alertsLoading } = useQuery({
    queryKey: ['alerts'],
    queryFn: () => api.getAlerts(),
    refetchInterval: 5000,
  })

  const router_health = systemStatus?.router_health

  return (
    <div className="min-h-screen p-6 relative z-10">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex justify-between items-center mb-4">
          <div>
            <h1 className="text-4xl font-bold gradient-text mb-2">
              🧠 منصة إدارة MikroTik الذكية
            </h1>
            <p className="text-dark-500 text-lg">
              مدعومة بالذكاء الصناعي المتقدم
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-dark-800">
              {currentTime.toLocaleTimeString('ar-SA')}
            </div>
            <div className="text-dark-500">
              {currentTime.toLocaleDateString('ar-SA', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* CPU Usage */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="card-hover"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="p-3 rounded-xl bg-primary-500/20 glow">
                <Cpu className="w-6 h-6 text-primary-400" />
              </div>
              <span className="text-2xl font-bold">
                {router_health?.cpu_usage?.toFixed(1) || 0}%
              </span>
            </div>
            <h3 className="text-dark-600 font-semibold mb-1">استخدام المعالج</h3>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${router_health?.cpu_usage || 0}%` }}
              />
            </div>
          </motion.div>

          {/* Memory Usage */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="card-hover"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="p-3 rounded-xl bg-accent-purple/20 glow-pink">
                <HardDrive className="w-6 h-6 text-accent-pink" />
              </div>
              <span className="text-2xl font-bold">
                {router_health?.memory_usage?.toFixed(1) || 0}%
              </span>
            </div>
            <h3 className="text-dark-600 font-semibold mb-1">استخدام الذاكرة</h3>
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${router_health?.memory_usage || 0}%` }}
              />
            </div>
          </motion.div>

          {/* Active Connections */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="card-hover"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="p-3 rounded-xl bg-accent-cyan/20 glow-cyan">
                <Users className="w-6 h-6 text-accent-cyan" />
              </div>
              <span className="text-2xl font-bold">
                {router_health?.active_connections || 0}
              </span>
            </div>
            <h3 className="text-dark-600 font-semibold mb-1">الاتصالات النشطة</h3>
            <p className="text-sm text-dark-500">
              {router_health?.interfaces_up || 0}/{router_health?.interfaces_total || 0} واجهات نشطة
            </p>
          </motion.div>

          {/* Health Score */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="card-hover"
          >
            <div className="flex items-center justify-between mb-3">
              <div className="p-3 rounded-xl bg-green-500/20 glow">
                <Activity className="w-6 h-6 text-green-400" />
              </div>
              <span className="text-2xl font-bold">
                {router_health?.health_score?.toFixed(0) || 0}
              </span>
            </div>
            <h3 className="text-dark-600 font-semibold mb-1">درجة الصحة</h3>
            <div className="flex items-center gap-2">
              <div 
                className={`status-dot ${
                  router_health?.status === 'healthy' ? 'status-healthy' :
                  router_health?.status === 'degraded' ? 'status-warning' :
                  'status-critical'
                }`} 
              />
              <span className="text-sm capitalize">{router_health?.status || 'unknown'}</span>
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* System Status */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-2"
        >
          <SystemStatus data={systemStatus} loading={statusLoading} />
        </motion.div>

        {/* Alerts Panel */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <AlertPanel alerts={alerts?.alerts || []} loading={alertsLoading} />
        </motion.div>
      </div>

      {/* Metrics Charts */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <MetricsChart data={metrics} loading={metricsLoading} />
      </motion.div>

      {/* AI Chat Widget */}
      <AIChatWidget />
    </div>
  )
}

export default Dashboard
