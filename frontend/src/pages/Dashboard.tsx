import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Activity, Cpu, HardDrive, Wifi, TrendingUp, AlertTriangle } from 'lucide-react'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { monitoringApi } from '@/lib/api'
import { wsManager } from '@/lib/websocket'

const COLORS = ['#00D9FF', '#FF00FF', '#00FF88', '#FFAA00']

export default function Dashboard() {
  const [monitoringData, setMonitoringData] = useState<any>({})
  const [alerts, setAlerts] = useState<any[]>([])
  const [chartData, setChartData] = useState<any[]>([])

  useEffect(() => {
    loadMonitoringData()

    // Connect to WebSocket for real-time updates
    wsManager.connectMonitoring((data) => {
      if (data.type === 'monitoring_update') {
        setMonitoringData((prev: any) => ({
          ...prev,
          [data.router_id]: data.data,
        }))

        if (data.alerts && data.alerts.length > 0) {
          setAlerts((prev) => [...prev, ...data.alerts])
        }

        // Update chart data
        setChartData((prev) => {
          const newData = [
            ...prev,
            {
              time: new Date().toLocaleTimeString('ar-EG'),
              cpu: data.data.cpu_load,
              memory: data.data.memory_usage,
            },
          ]
          return newData.slice(-20) // Keep last 20 points
        })
      }
    })

    return () => {
      wsManager.disconnectMonitoring()
    }
  }, [])

  const loadMonitoringData = async () => {
    try {
      const response = await monitoringApi.getAllRoutersStatus()
      setMonitoringData(response.data)
    } catch (error) {
      console.error('Error loading monitoring data:', error)
    }
  }

  const stats = [
    {
      label: '?????? ?????????',
      value: Object.keys(monitoringData).length || 0,
      icon: Wifi,
      color: 'text-primary',
    },
    {
      label: '??????',
      value: Object.values(monitoringData).filter((r: any) => !r.error).length,
      icon: Activity,
      color: 'text-green-400',
    },
    {
      label: '????? CPU',
      value: `${Object.values(monitoringData).reduce((acc: number, r: any) => acc + (r.cpu_load || 0), 0) / Math.max(Object.keys(monitoringData).length, 1)}%`,
      icon: Cpu,
      color: 'text-yellow-400',
    },
    {
      label: '????? ???????',
      value: `${Object.values(monitoringData).reduce((acc: number, r: any) => acc + (r.memory_usage || 0), 0) / Math.max(Object.keys(monitoringData).length, 1)}%`,
      icon: HardDrive,
      color: 'text-secondary',
    },
  ]

  const pieData = [
    { name: 'CPU', value: Object.values(monitoringData).reduce((acc: number, r: any) => acc + (r.cpu_load || 0), 0) / Math.max(Object.keys(monitoringData).length, 1) },
    { name: 'Memory', value: Object.values(monitoringData).reduce((acc: number, r: any) => acc + (r.memory_usage || 0), 0) / Math.max(Object.keys(monitoringData).length, 1) },
  ]

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold glow-text text-primary mb-2">???? ??????</h1>
          <p className="text-gray-400">?????? ????? ????? MikroTik</p>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="glass-effect rounded-xl p-6 border border-primary/20"
            >
              <div className="flex items-center justify-between mb-4">
                <Icon className={`w-8 h-8 ${stat.color}`} />
                <TrendingUp className="w-5 h-5 text-green-400" />
              </div>
              <h3 className="text-2xl font-bold mb-1">{stat.value}</h3>
              <p className="text-sm text-gray-400">{stat.label}</p>
            </motion.div>
          )
        })}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-effect rounded-xl p-6 border border-primary/20"
        >
          <h2 className="text-xl font-bold mb-4 text-primary">?????? ??????</h2>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#00D9FF" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#00D9FF" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorMemory" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#FF00FF" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#FF00FF" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#2A2A3E" />
              <XAxis dataKey="time" stroke="#666" />
              <YAxis stroke="#666" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1A1A2E',
                  border: '1px solid #00D9FF',
                  borderRadius: '8px',
                }}
              />
              <Area
                type="monotone"
                dataKey="cpu"
                stroke="#00D9FF"
                fillOpacity={1}
                fill="url(#colorCpu)"
                name="CPU %"
              />
              <Area
                type="monotone"
                dataKey="memory"
                stroke="#FF00FF"
                fillOpacity={1}
                fill="url(#colorMemory)"
                name="Memory %"
              />
            </AreaChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-effect rounded-xl p-6 border border-primary/20"
        >
          <h2 className="text-xl font-bold mb-4 text-primary">????? ???????</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1A1A2E',
                  border: '1px solid #00D9FF',
                  borderRadius: '8px',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-effect rounded-xl p-6 border border-yellow-500/30"
        >
          <div className="flex items-center gap-3 mb-4">
            <AlertTriangle className="w-6 h-6 text-yellow-400" />
            <h2 className="text-xl font-bold text-yellow-400">?????????</h2>
          </div>
          <div className="space-y-2">
            {alerts.slice(-5).map((alert, index) => (
              <div key={index} className="flex items-center gap-3 p-3 bg-dark-lighter rounded-lg">
                <div className={`w-2 h-2 rounded-full ${
                  alert.severity === 'error' ? 'bg-red-500' : 'bg-yellow-500'
                }`}></div>
                <p className="text-sm">{alert.message}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  )
}
