import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Activity, Cpu, HardDrive, Wifi, AlertTriangle, Router } from 'lucide-react'
import { monitoringApi } from '@/lib/api'
import { wsManager } from '@/lib/websocket'

export default function Monitoring() {
  const [monitoringData, setMonitoringData] = useState<Record<string, any>>({})
  const [selectedRouter, setSelectedRouter] = useState<string | null>(null)

  useEffect(() => {
    loadMonitoringData()

    wsManager.connectMonitoring((data) => {
      if (data.type === 'monitoring_update') {
        setMonitoringData((prev) => ({
          ...prev,
          [data.router_id]: data.data,
        }))
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

  const routerIds = Object.keys(monitoringData)

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold glow-text text-primary mb-2">???????? ???????</h1>
          <p className="text-gray-400">?????? ?????? ????? ?????????</p>
        </div>
      </motion.div>

      {/* Router List */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {routerIds.map((routerId, index) => {
          const data = monitoringData[routerId]
          const isSelected = selectedRouter === routerId

          return (
            <motion.div
              key={routerId}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              onClick={() => setSelectedRouter(isSelected ? null : routerId)}
              className={`glass-effect rounded-xl p-6 border cursor-pointer transition-all ${
                isSelected ? 'border-primary border-2' : 'border-primary/20 hover:border-primary/50'
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center">
                    <Router className="w-6 h-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">{routerId}</h3>
                    <p className="text-sm text-gray-400">????: {data.error ? '???' : '???'}</p>
                  </div>
                </div>
                <Activity className={`w-5 h-5 ${data.error ? 'text-red-400' : 'text-green-400'}`} />
              </div>

              {!data.error && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Cpu className="w-4 h-4 text-yellow-400" />
                      <span className="text-sm">CPU</span>
                    </div>
                    <span className="font-bold">{data.cpu_load?.toFixed(1) || 0}%</span>
                  </div>
                  <div className="w-full bg-dark-lighter rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${data.cpu_load || 0}%` }}
                      className="bg-yellow-400 h-2 rounded-full"
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <HardDrive className="w-4 h-4 text-secondary" />
                      <span className="text-sm">???????</span>
                    </div>
                    <span className="font-bold">{data.memory_usage?.toFixed(1) || 0}%</span>
                  </div>
                  <div className="w-full bg-dark-lighter rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${data.memory_usage || 0}%` }}
                      className="bg-secondary h-2 rounded-full"
                    />
                  </div>

                  {data.interfaces && (
                    <div className="pt-3 border-t border-primary/20">
                      <div className="flex items-center gap-2 mb-2">
                        <Wifi className="w-4 h-4 text-primary" />
                        <span className="text-sm font-medium">????????</span>
                      </div>
                      <div className="space-y-1">
                        {data.interfaces.slice(0, 3).map((iface: any, idx: number) => (
                          <div key={idx} className="flex items-center justify-between text-xs">
                            <span className="text-gray-400">{iface.name}</span>
                            <span className={iface.running ? 'text-green-400' : 'text-red-400'}>
                              {iface.running ? '???' : '??? ???'}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          )
        })}
      </div>

      {routerIds.length === 0 && (
        <div className="text-center py-12 glass-effect rounded-xl border border-primary/20">
          <Activity className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">?? ???? ??????? ????????</p>
        </div>
      )}
    </div>
  )
}
