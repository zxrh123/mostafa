import { motion } from 'framer-motion';

interface MetricCardProps {
  title: string;
  value: string;
  subtitle?: string;
  trend?: 'up' | 'down' | 'stable';
}

export function MetricCard({ title, value, subtitle, trend = 'stable' }: MetricCardProps) {
  const trendColor = trend === 'up' ? 'text-emerald-400' : trend === 'down' ? 'text-rose-400' : 'text-blue-300';

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-panel p-6 space-y-4"
    >
      <div className="text-sm text-white/60">{title}</div>
      <div className="flex items-end justify-between">
        <span className="text-4xl font-extrabold text-white">{value}</span>
        <span className={`text-xs font-semibold ${trendColor}`}>
          {trend === 'up' && '? ????'}
          {trend === 'down' && '? ??????'}
          {trend === 'stable' && '? ????'}
        </span>
      </div>
      {subtitle && <p className="text-xs text-white/50">{subtitle}</p>}
    </motion.div>
  );
}
