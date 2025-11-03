import { ReactNode } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Bot, Gauge, RadioTower, ShieldAlert } from 'lucide-react';

interface BaseLayoutProps {
  children: ReactNode;
}

const navItems = [
  { to: '/', label: '???? ??????', icon: Gauge },
  { to: '/automation', label: '??????? ??????', icon: Bot },
  { to: '/hotspot', label: '????? ????? ????', icon: RadioTower },
  { to: '/security', label: '????? ?????????', icon: ShieldAlert }
];

export function BaseLayout({ children }: BaseLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-midnight via-slate to-midnight text-white">
      <header className="flex items-center justify-between px-8 py-6 backdrop-blur-xl bg-black/40 border-b border-white/10">
        <Link to="/" className="flex items-center gap-3">
          <motion.div
            initial={{ rotate: -15, scale: 0.8 }}
            animate={{ rotate: 0, scale: 1 }}
            transition={{ type: 'spring', stiffness: 200 }}
            className="p-3 rounded-2xl bg-gradient-to-br from-neon/40 to-magenta/40 shadow-xl"
          >
            <Bot className="w-6 h-6 text-neon" />
          </motion.div>
          <div>
            <p className="text-xl font-semibold gradient-text">MikroTik AI Brain</p>
            <p className="text-xs text-neon/70">????? ??????? ?????? ???????</p>
          </div>
        </Link>
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-panel px-6 py-3 flex items-center gap-4"
        >
          <span className="text-sm text-neon/80">????? ?????? ??????</span>
          <div className="flex items-center gap-1 text-xs text-white/70">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>?????? ???? ????...</span>
          </div>
        </motion.div>
      </header>
      <div className="flex flex-1">
        <aside className="w-72 px-6 py-8 border-r border-white/5 bg-black/30 backdrop-blur-xl">
          <nav className="flex flex-col gap-2">
            {navItems.map(({ to, label, icon: Icon }) => (
              <NavLink
                key={to}
                to={to}
                end={to === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-2xl transition-all ${
                    isActive
                      ? 'glass-panel border-neon/40 shadow-neon'
                      : 'hover:bg-white/5 text-white/70'
                  }`
                }
              >
                <Icon className="w-5 h-5" />
                <span className="text-sm font-semibold">{label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>
        <main className="flex-1 p-8 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}
