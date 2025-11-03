import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Plus, Router, Trash2, Power, PowerOff } from 'lucide-react'
import { routerApi } from '@/lib/api'

interface Router {
  router_id: string
  name: string
  host: string
  is_connected: boolean
}

export default function Routers() {
  const [routers, setRouters] = useState<Router[]>([])
  const [loading, setLoading] = useState(true)
  const [showAddModal, setShowAddModal] = useState(false)
  const [formData, setFormData] = useState({
    router_id: '',
    name: '',
    host: '',
    username: '',
    password: '',
    api_port: 8728,
  })

  useEffect(() => {
    loadRouters()
  }, [])

  const loadRouters = async () => {
    try {
      const response = await routerApi.list()
      setRouters(response.data)
    } catch (error) {
      console.error('Error loading routers:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = async () => {
    try {
      await routerApi.add(formData)
      setShowAddModal(false)
      setFormData({
        router_id: '',
        name: '',
        host: '',
        username: '',
        password: '',
        api_port: 8728,
      })
      loadRouters()
    } catch (error: any) {
      alert(error.response?.data?.detail || '??? ???')
    }
  }

  const handleRemove = async (routerId: string) => {
    if (!confirm('?? ??? ????? ?? ??? ??? ????????')) return

    try {
      await routerApi.remove(routerId)
      loadRouters()
    } catch (error: any) {
      alert(error.response?.data?.detail || '??? ???')
    }
  }

  if (loading) {
    return <div className="text-center py-12">???? ???????...</div>
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold glow-text text-primary mb-2">????? ?????????</h1>
          <p className="text-gray-400">????? ?????? ????? MikroTik</p>
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary to-secondary rounded-lg font-medium hover:shadow-lg hover:shadow-primary/50 transition-all"
        >
          <Plus className="w-5 h-5" />
          ????? ?????
        </motion.button>
      </motion.div>

      {/* Routers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {routers.map((router, index) => (
          <motion.div
            key={router.router_id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-effect rounded-xl p-6 border border-primary/20 hover:border-primary/50 transition-all"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                  router.is_connected ? 'bg-green-500/20' : 'bg-red-500/20'
                }`}>
                  <Router className={`w-6 h-6 ${
                    router.is_connected ? 'text-green-400' : 'text-red-400'
                  }`} />
                </div>
                <div>
                  <h3 className="font-bold text-lg">{router.name}</h3>
                  <p className="text-sm text-gray-400">{router.host}</p>
                </div>
              </div>
              <button
                onClick={() => handleRemove(router.router_id)}
                className="p-2 hover:bg-red-500/20 rounded-lg transition-colors"
              >
                <Trash2 className="w-5 h-5 text-red-400" />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                {router.is_connected ? (
                  <>
                    <Power className="w-4 h-4 text-green-400" />
                    <span className="text-sm text-green-400">????</span>
                  </>
                ) : (
                  <>
                    <PowerOff className="w-4 h-4 text-red-400" />
                    <span className="text-sm text-red-400">??? ????</span>
                  </>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {routers.length === 0 && (
        <div className="text-center py-12 glass-effect rounded-xl border border-primary/20">
          <Router className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">?? ???? ??????? ?????</p>
        </div>
      )}

      {/* Add Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-effect rounded-xl p-6 border border-primary/30 w-full max-w-md"
          >
            <h2 className="text-2xl font-bold mb-6 text-primary">????? ????? ????</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">???? ???????</label>
                <input
                  type="text"
                  value={formData.router_id}
                  onChange={(e) => setFormData({ ...formData, router_id: e.target.value })}
                  className="w-full px-4 py-2 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">?????</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">????? IP</label>
                <input
                  type="text"
                  value={formData.host}
                  onChange={(e) => setFormData({ ...formData, host: e.target.value })}
                  className="w-full px-4 py-2 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">??? ????????</label>
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full px-4 py-2 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">???? ??????</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full px-4 py-2 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">???? API</label>
                <input
                  type="number"
                  value={formData.api_port}
                  onChange={(e) => setFormData({ ...formData, api_port: parseInt(e.target.value) })}
                  className="w-full px-4 py-2 bg-dark-lighter border border-primary/20 rounded-lg focus:outline-none focus:border-primary"
                />
              </div>
            </div>
            <div className="flex gap-4 mt-6">
              <button
                onClick={() => setShowAddModal(false)}
                className="flex-1 px-4 py-2 bg-dark-lighter rounded-lg hover:bg-dark-lightest transition-colors"
              >
                ?????
              </button>
              <button
                onClick={handleAdd}
                className="flex-1 px-4 py-2 bg-gradient-to-r from-primary to-secondary rounded-lg font-medium hover:shadow-lg transition-all"
              >
                ?????
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  )
}
