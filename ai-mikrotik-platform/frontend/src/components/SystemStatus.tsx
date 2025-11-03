import { motion } from 'framer-motion'
import { Server, Cpu, Database, Activity, CheckCircle, AlertTriangle } from 'lucide-react'

interface SystemStatusProps {
  data: any
  loading: boolean
}

const SystemStatus = ({ data, loading }: SystemStatusProps) => {
  if (loading) {
    return (
      <div className="card h-full">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-white/10 rounded w-1/3" />
          <div className="space-y-2">
            <div className="h-16 bg-white/10 rounded" />
            <div className="h-16 bg-white/10 rounded" />
            <div className="h-16 bg-white/10 rounded" />
          </div>
        </div>
      </div>
    )
  }

  const components = data?.system || {}
  const ai_brain = components.ai_brain || {}
  const executor = components.executor || {}
  const monitor = components.monitor || {}

  return (
    <div className="card h-full">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Server className="w-6 h-6 text-primary-400" />
        حالة النظام
      </h2>

      <div className="space-y-4">
        {/* AI Brain Status */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass p-4 rounded-xl"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-primary-400" />
              <span className="font-semibold">العقل الصناعي (AI Brain)</span>
            </div>
            {ai_brain.status === 'active' ? (
              <CheckCircle className="w-5 h-5 text-green-400" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-red-400" />
            )}
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-dark-500">الحالة:</span>
              <span className="font-semibold mr-2">{ai_brain.status || 'غير معروف'}</span>
            </div>
            <div>
              <span className="text-dark-500">القرارات المتخذة:</span>
              <span className="font-semibold mr-2">{ai_brain.total_decisions || 0}</span>
            </div>
            <div>
              <span className="text-dark-500">التعلم التلقائي:</span>
              <span className="font-semibold mr-2">
                {ai_brain.learning_enabled ? '✅ مفعل' : '❌ معطل'}
              </span>
            </div>
            <div>
              <span className="text-dark-500">قاعدة المعرفة:</span>
              <span className="font-semibold mr-2">{ai_brain.knowledge_base_size || 0} عنصر</span>
            </div>
          </div>
        </motion.div>

        {/* Executor Status */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass p-4 rounded-xl"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <Cpu className="w-5 h-5 text-accent-cyan" />
              <span className="font-semibold">محرك التنفيذ (Executor)</span>
            </div>
            {executor.connected ? (
              <CheckCircle className="w-5 h-5 text-green-400" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-red-400" />
            )}
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-dark-500">الاتصال:</span>
              <span className="font-semibold mr-2">
                {executor.connected ? '✅ متصل' : '❌ غير متصل'}
              </span>
            </div>
            <div>
              <span className="text-dark-500">التنفيذات:</span>
              <span className="font-semibold mr-2">{executor.executions_count || 0}</span>
            </div>
          </div>
        </motion.div>

        {/* Monitor Status */}
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="glass p-4 rounded-xl"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-3">
              <Database className="w-5 h-5 text-accent-pink" />
              <span className="font-semibold">محرك المراقبة (Monitor)</span>
            </div>
            {monitor.is_monitoring ? (
              <CheckCircle className="w-5 h-5 text-green-400" />
            ) : (
              <AlertTriangle className="w-5 h-5 text-red-400" />
            )}
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-dark-500">الحالة:</span>
              <span className="font-semibold mr-2">
                {monitor.is_monitoring ? '🟢 نشط' : '🔴 متوقف'}
              </span>
            </div>
            <div>
              <span className="text-dark-500">التنبيهات النشطة:</span>
              <span className="font-semibold mr-2">{monitor.active_alerts || 0}</span>
            </div>
            <div className="col-span-2">
              <span className="text-dark-500">المقاييس المجمعة:</span>
              <span className="font-semibold mr-2">{monitor.total_metrics_collected || 0}</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default SystemStatus
