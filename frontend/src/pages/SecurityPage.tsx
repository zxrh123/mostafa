import { motion } from 'framer-motion';
import { AlertTriangle, ShieldCheck, ShieldHalf, TerminalSquare } from 'lucide-react';

const intrusionEvents = [
  { id: 'evt-1', source: '41.215.22.10', vector: 'Brute Force Login', action: 'Blocked + rate-limited' },
  { id: 'evt-2', source: '185.33.71.9', vector: 'Malformed DNS Queries', action: 'Quarantined subnet' },
  { id: 'evt-3', source: '10.12.55.34', vector: 'Abnormal traffic spike', action: 'AI load balance reroute' }
];

const logLines = [
  '14:22:01 [AI-SEC] anomaly=zombie-session host=10.0.0.1 severity=high mitigated=true',
  '14:21:35 [AI-SEC] login-attempt user=admin host=10.0.0.2 result=denied count=5',
  '14:20:17 [AI-SEC] ddos-probe source=185.33.71.9 action=null-route duration=900s'
];

export function SecurityPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }} className="space-y-8">
      <section className="glass-panel p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="p-4 rounded-3xl bg-gradient-to-br from-magenta/30 to-red-400/20">
            <ShieldHalf className="w-7 h-7 text-magenta" />
          </span>
          <div>
            <h2 className="text-lg font-semibold text-white">???? ?????? ?????</h2>
            <p className="text-sm text-white/60">????? ???? ?????? RouterOS? ?????? ?????????? ???????? ????? ???????.</p>
          </div>
        </div>
        <ShieldCheck className="w-6 h-6 text-emerald-400" />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-sm text-white/70 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-magenta" /> ????? ?????? ???????
          </h3>
          <div className="space-y-3 text-xs text-white/70">
            {intrusionEvents.map((event) => (
              <div key={event.id} className="bg-black/30 rounded-2xl px-4 py-3 border border-white/5">
                <p className="text-sm text-white">{event.vector}</p>
                <p className="mt-1">??????: {event.source}</p>
                <p className="mt-1 text-emerald-300">???????: {event.action}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="glass-panel p-6 space-y-4">
          <h3 className="text-sm text-white/70 flex items-center gap-2">
            <TerminalSquare className="w-4 h-4 text-neon" /> ????? ?????? ???????
          </h3>
          <pre className="bg-black/60 rounded-2xl p-4 text-xs text-neon/90 leading-relaxed overflow-x-auto">
            {logLines.join('\n')}
          </pre>
        </div>
      </section>
    </motion.div>
  );
}
