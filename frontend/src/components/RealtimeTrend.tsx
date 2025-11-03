import { motion } from 'framer-motion';

interface RealtimeTrendProps {
  title: string;
  data: number[];
  unit?: string;
}

export function RealtimeTrend({ title, data, unit }: RealtimeTrendProps) {
  const max = Math.max(...data, 1);

  return (
    <div className="glass-panel p-6 h-64 flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm text-white/60">{title}</h3>
        <span className="text-sm text-neon/80">??? ????? ????</span>
      </div>
      <div className="flex-1 relative">
        <svg viewBox="0 0 100 40" className="w-full h-full">
          <defs>
            <linearGradient id={`${title}-gradient`} x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stopColor="#4de4ff" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#4de4ff" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            d={`M0,40 ${data
              .map((value, index) => `L ${(index / (data.length - 1)) * 100},${40 - (value / max) * 35}`)
              .join(' ')} L100,40 Z`}
            fill={`url(#${title}-gradient)`}
            stroke="#4de4ff"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
        </svg>
        <motion.div
          key={data[data.length - 1]}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="absolute bottom-4 right-4 text-right"
        >
          <div className="text-3xl font-bold text-white">
            {data[data.length - 1].toFixed(1)} {unit}
          </div>
          <div className="text-xs text-white/50">????? ??? 5 ?????</div>
        </motion.div>
      </div>
    </div>
  );
}
