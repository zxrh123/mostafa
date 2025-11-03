import { motion } from 'framer-motion';
import { Wifi, MessageCircle } from 'lucide-react';

import { AIChatWidget } from '../components/AIChatWidget';

const text = {
  heroTitle: '\u0646\u0642\u0637\u0629 \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0627\u0644\u0630\u0643\u064a\u0629',
  heroDescription:
    '\u064a\u062f\u064a\u0631 \u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0635\u0646\u0627\u0639\u064a \u0627\u0644\u0628\u0648\u0627\u0628\u0629\u060c \u064a\u062a\u0648\u0627\u0635\u0644 \u0645\u0639 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646\u060c \u0648\u064a\u0636\u0628\u0637 \u0627\u0644\u0633\u064a\u0627\u0633\u0627\u062a \u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u064b\u0627 \u062d\u0633\u0628 \u0627\u0644\u0633\u0644\u0648\u0643.',
  statSessions: '\u062c\u0644\u0633\u0627\u062a \u0646\u0634\u0637\u0629 \u0627\u0644\u0622\u0646',
  statSessionsDesc: '\u0645\u062d\u062f\u062b \u0622\u0644\u064a\u064b\u0627 \u0643\u0644 5 \u062b\u0648\u0627\u0646\u064d',
  statSatisfaction: '\u0646\u0633\u0628\u0629 \u0627\u0644\u0631\u0636\u0627',
  statSatisfactionDesc: '\u062d\u0633\u0628 \u062a\u0642\u064a\u064a\u0645\u0627\u062a \u0627\u0644\u0645\u0633\u0627\u0639\u062f',
  statIncidents: '\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0625\u0635\u0644\u0627\u062d',
  statIncidentsDesc: '\u062a\u0645 \u062d\u0644 6 \u062a\u0644\u0642\u0627\u0626\u064a\u064b\u0627',
  statMessages: '\u0631\u0633\u0627\u0626\u0644 \u0627\u0644\u064a\u0648\u0645',
  statMessagesDesc: '\u062a\u0645 \u0627\u0644\u0631\u062f \u062e\u0644\u0627\u0644 2.4 \u062b\u0627\u0646\u064a\u0629',
  scenarioTitle: '\u0633\u064a\u0646\u0627\u0631\u064a\u0648\u0647\u0627\u062a \u0627\u0644\u062a\u0641\u0627\u0639\u0644 \u0627\u0644\u0630\u0643\u064a',
  scenario1:
    '\u0645\u0639\u0627\u0644\u062c\u0629 \u0637\u0644\u0628\u0627\u062a \u0625\u0639\u0627\u062f\u0629 \u0627\u0644\u062a\u0648\u062c\u064a\u0647 \u0648\u0625\u0631\u0633\u0627\u0644 \u0627\u0644\u062a\u0630\u0627\u0643\u0631 \u0625\u0644\u0649 \u0627\u0644\u0641\u0646\u064a\u064a\u0646 \u062a\u0644\u0642\u0627\u0626\u064a\u064b\u0627.',
  scenario2: '\u062a\u0639\u062f\u064a\u0644 \u0633\u0631\u0639\u0627\u062a \u0627\u0644\u062d\u0632\u0645 \u0639\u0646\u062f \u0627\u0643\u062a\u0634\u0627\u0641 \u0636\u063a\u0637 \u0643\u0628\u064a\u0631 \u0639\u0644\u0649 \u0627\u0644\u0634\u0628\u0643\u0629.',
  scenario3:
    '\u0625\u0631\u0633\u0627\u0644 \u0631\u0633\u0627\u0626\u0644 \u0625\u0631\u0634\u0627\u062f\u064a\u0629 \u0644\u0644\u0639\u0645\u0644\u0627\u0621 \u0627\u0644\u0630\u064a\u0646 \u064a\u0639\u0627\u0646\u0648\u0646 \u0645\u0646 \u0636\u0639\u0641 \u0627\u0644\u0627\u062a\u0635\u0627\u0644.'
};

export function HotspotPage() {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AIChatWidget />
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-panel p-6 space-y-6"
        >
          <div className="flex items-center gap-3">
            <span className="p-3 rounded-2xl bg-gradient-to-br from-neon/20 to-magenta/20">
              <Wifi className="w-6 h-6 text-neon" />
            </span>
            <div>
              <h3 className="text-sm font-semibold text-white">{text.heroTitle}</h3>
              <p className="text-xs text-white/60">{text.heroDescription}</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs text-white/70">
            <div className="bg-black/30 rounded-2xl px-4 py-3">
              <p>{text.statSessions}</p>
              <p className="text-2xl font-bold text-white">128</p>
              <p className="text-[10px] text-white/40">{text.statSessionsDesc}</p>
            </div>
            <div className="bg-black/30 rounded-2xl px-4 py-3">
              <p>{text.statSatisfaction}</p>
              <p className="text-2xl font-bold text-white">96%</p>
              <p className="text-[10px] text-white/40">{text.statSatisfactionDesc}</p>
            </div>
            <div className="bg-black/30 rounded-2xl px-4 py-3">
              <p>{text.statIncidents}</p>
              <p className="text-2xl font-bold text-white">7</p>
              <p className="text-[10px] text-white/40">{text.statIncidentsDesc}</p>
            </div>
            <div className="bg-black/30 rounded-2xl px-4 py-3">
              <p>{text.statMessages}</p>
              <p className="text-2xl font-bold text-white">342</p>
              <p className="text-[10px] text-white/40">{text.statMessagesDesc}</p>
            </div>
          </div>
          <div className="glass-panel bg-white/5 border border-white/10 rounded-3xl p-4 space-y-2">
            <h4 className="text-sm text-white/80 flex items-center gap-2">
              <MessageCircle className="w-4 h-4 text-neon" /> {text.scenarioTitle}
            </h4>
            <ul className="text-xs text-white/70 space-y-2 leading-relaxed">
              <li>{text.scenario1}</li>
              <li>{text.scenario2}</li>
              <li>{text.scenario3}</li>
            </ul>
          </div>
        </motion.div>
      </section>
    </motion.div>
  );
}
