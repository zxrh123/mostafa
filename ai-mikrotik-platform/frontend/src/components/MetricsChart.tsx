import { motion } from 'framer-motion'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { TrendingUp } from 'lucide-react'

interface MetricsChartProps {
  data: any
  loading: boolean
}

const MetricsChart = ({ data, loading }: MetricsChartProps) => {
  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-white/10 rounded w-1/3" />
          <div className="h-64 bg-white/10 rounded" />
        </div>
      </div>
    )
  }

  // تحضير البيانات للرسم البياني
  const chartData = Object.entries(data || {}).map(([key, value]: [string, any]) => ({
    name: key,
    current: value.current || 0,
    average: value.average || 0,
    max: value.max || 0,
    min: value.min || 0,
  }))

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <TrendingUp className="w-6 h-6 text-primary-400" />
        المقاييس اللحظية
      </h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CPU & Memory Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass p-4 rounded-xl"
        >
          <h3 className="text-lg font-semibold mb-4">المعالج والذاكرة</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={chartData.filter(d => ['cpu', 'memory'].includes(d.name))}>
              <defs>
                <linearGradient id="colorCPU" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#1890ff" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#1890ff" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="colorMemory" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ff006e" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#ff006e" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" />
              <YAxis stroke="rgba(255,255,255,0.5)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.8)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                }}
              />
              <Area
                type="monotone"
                dataKey="current"
                stroke="#1890ff"
                fillOpacity={1}
                fill="url(#colorCPU)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Bandwidth Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass p-4 rounded-xl"
        >
          <h3 className="text-lg font-semibold mb-4">النطاق الترددي</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData.filter(d => ['bandwidth'].includes(d.name))}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" />
              <YAxis stroke="rgba(255,255,255,0.5)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.8)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                }}
              />
              <Line
                type="monotone"
                dataKey="current"
                stroke="#00f5d4"
                strokeWidth={3}
                dot={{ fill: '#00f5d4', r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="average"
                stroke="#ff9e00"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Connections Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass p-4 rounded-xl"
        >
          <h3 className="text-lg font-semibold mb-4">الاتصالات</h3>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={chartData.filter(d => ['connections'].includes(d.name))}>
              <defs>
                <linearGradient id="colorConnections" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#7209b7" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#7209b7" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" stroke="rgba(255,255,255,0.5)" />
              <YAxis stroke="rgba(255,255,255,0.5)" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0,0,0,0.8)',
                  border: '1px solid rgba(255,255,255,0.2)',
                  borderRadius: '8px',
                }}
              />
              <Area
                type="monotone"
                dataKey="current"
                stroke="#7209b7"
                fillOpacity={1}
                fill="url(#colorConnections)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Statistics Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass p-4 rounded-xl"
        >
          <h3 className="text-lg font-semibold mb-4">إحصائيات عامة</h3>
          <div className="space-y-3">
            {chartData.slice(0, 4).map((metric, index) => (
              <div key={index} className="flex items-center justify-between">
                <span className="text-sm text-dark-600 capitalize">{metric.name}</span>
                <div className="flex items-center gap-4 text-sm">
                  <div>
                    <span className="text-dark-500">الحالي: </span>
                    <span className="font-bold text-primary-400">{metric.current.toFixed(1)}</span>
                  </div>
                  <div>
                    <span className="text-dark-500">المتوسط: </span>
                    <span className="font-bold text-dark-700">{metric.average.toFixed(1)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default MetricsChart
