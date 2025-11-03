import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  LayoutDashboard, 
  Router, 
  Activity, 
  MessageCircle,
  Sparkles
} from 'lucide-react'

interface LayoutProps {
  children: ReactNode
}

const navItems = [
  { path: '/', icon: LayoutDashboard, label: '???? ??????' },
  { path: '/routers', icon: Router, label: '?????????' },
  { path: '/monitoring', icon: Activity, label: '????????' },
  { path: '/chat', icon: MessageCircle, label: '??????? ?????' },
]

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-dark flex">
      {/* Sidebar */}
      <motion.aside
        initial={{ x: -100 }}
        animate={{ x: 0 }}
        className="w-64 glass-effect border-r border-primary/20 p-6"
      >
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-lg flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-dark" />
          </div>
          <div>
            <h1 className="text-xl font-bold glow-text text-primary">MikroTik AI</h1>
            <p className="text-xs text-gray-400">???? ????? ???</p>
          </div>
        </div>

        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                  isActive
                    ? 'bg-primary/20 text-primary border border-primary/30'
                    : 'text-gray-300 hover:bg-dark-lighter hover:text-primary'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            )
          })}
        </nav>

        <div className="mt-8 p-4 glass-effect rounded-lg border border-primary/20">
          <div className="flex items-center gap-2 mb-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-gray-300">AI Brain ???</span>
          </div>
          <p className="text-xs text-gray-400">?????? ???? ?????? 100%</p>
        </div>
      </motion.aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="p-8"
        >
          {children}
        </motion.div>
      </main>
    </div>
  )
}
