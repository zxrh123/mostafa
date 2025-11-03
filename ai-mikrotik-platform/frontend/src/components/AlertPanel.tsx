import { motion, AnimatePresence } from 'framer-motion'
import { AlertCircle, AlertTriangle, Info, XCircle } from 'lucide-react'

interface Alert {
  id: string
  level: string
  title: string
  message: string
  metric_type: string
  current_value: number
  threshold: number
  timestamp: string
  resolved: boolean
}

interface AlertPanelProps {
  alerts: Alert[]
  loading: boolean
}

const AlertPanel = ({ alerts, loading }: AlertPanelProps) => {
  if (loading) {
    return (
      <div className="card h-full">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-white/10 rounded w-1/2" />
          <div className="space-y-2">
            <div className="h-20 bg-white/10 rounded" />
            <div className="h-20 bg-white/10 rounded" />
          </div>
        </div>
      </div>
    )
  }

  const getAlertIcon = (level: string) => {
    switch (level) {
      case 'emergency':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'critical':
        return <AlertCircle className="w-5 h-5 text-red-400" />
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-400" />
      default:
        return <Info className="w-5 h-5 text-blue-400" />
    }
  }

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'emergency':
        return 'border-red-500 bg-red-500/10'
      case 'critical':
        return 'border-red-400 bg-red-400/10'
      case 'warning':
        return 'border-yellow-400 bg-yellow-400/10'
      default:
        return 'border-blue-400 bg-blue-400/10'
    }
  }

  return (
    <div className="card h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold flex items-center gap-2">
          <AlertCircle className="w-6 h-6 text-red-400" />
          التنبيهات
        </h2>
        <span className="px-3 py-1 rounded-full glass text-sm font-semibold">
          {alerts.filter(a => !a.resolved).length} نشط
        </span>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3">
        <AnimatePresence>
          {alerts.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex flex-col items-center justify-center h-full text-center py-12"
            >
              <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mb-4">
                <AlertCircle className="w-8 h-8 text-green-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">لا توجد تنبيهات</h3>
              <p className="text-dark-500 text-sm">
                النظام يعمل بشكل طبيعي
              </p>
            </motion.div>
          ) : (
            alerts.map((alert, index) => (
              <motion.div
                key={alert.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ delay: index * 0.1 }}
                className={`glass rounded-xl p-4 border-l-4 ${getAlertColor(alert.level)}`}
              >
                <div className="flex items-start gap-3">
                  {getAlertIcon(alert.level)}
                  <div className="flex-1">
                    <h3 className="font-semibold mb-1">{alert.title}</h3>
                    <p className="text-sm text-dark-600 mb-2">{alert.message}</p>
                    <div className="flex items-center justify-between text-xs text-dark-500">
                      <span>
                        {alert.metric_type} • {alert.current_value.toFixed(1)}
                      </span>
                      <span>
                        {new Date(alert.timestamp).toLocaleTimeString('ar-SA')}
                      </span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}

export default AlertPanel
