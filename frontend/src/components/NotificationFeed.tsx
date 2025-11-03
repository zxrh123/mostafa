import { motion } from 'framer-motion';
import { AlertTriangle, Activity, BrainCircuit } from 'lucide-react';

interface Notification {
  id: string;
  title: string;
  message: string;
  severity: 'info' | 'warning' | 'critical';
  timestamp: string;
}

interface NotificationFeedProps {
  items: Notification[];
}

const iconMap = {
  info: BrainCircuit,
  warning: Activity,
  critical: AlertTriangle
};

const severityGradient: Record<Notification['severity'], string> = {
  info: 'from-neon/40 to-blue-500/20',
  warning: 'from-amber-400/40 to-orange-500/20',
  critical: 'from-rose-500/50 to-red-500/20'
};

export function NotificationFeed({ items }: NotificationFeedProps) {
  return (
    <div className="glass-panel p-6 space-y-4 h-full overflow-y-auto">
      <h3 className="text-sm text-white/70">??????? ????????? ?????? ???????</h3>
      <div className="space-y-3">
        {items.map((item) => {
          const Icon = iconMap[item.severity];
          return (
            <motion.div
              key={item.id}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className={`relative p-4 rounded-2xl bg-gradient-to-r ${severityGradient[item.severity]} border border-white/10`}
            >
              <div className="flex items-start gap-3">
                <span className="p-2 rounded-xl bg-black/20">
                  <Icon className="w-5 h-5 text-white" />
                </span>
                <div>
                  <p className="text-sm font-semibold text-white">{item.title}</p>
                  <p className="text-xs text-white/70 mt-1 leading-relaxed">{item.message}</p>
                </div>
                <span className="text-[10px] text-white/50 ml-auto">{item.timestamp}</span>
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
