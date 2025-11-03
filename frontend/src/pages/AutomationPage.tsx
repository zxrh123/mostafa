import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Bot, Repeat2, ShieldPlus, Sparkles } from 'lucide-react';

import { api } from '../lib/api';

interface AutomationToggle {
  feature: string;
  enabled: boolean;
  updated_at: string;
}

const text = {
  autoExecuteDesc:
    '\u062a\u0646\u0641\u064a\u0630 \u0623\u0648\u0627\u0645\u0631 \u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0635\u0646\u0627\u0639\u064a \u062a\u0644\u0642\u0627\u0626\u064a\u064b\u0627 \u0628\u0639\u062f \u0641\u062d\u0635 \u0627\u0644\u0633\u0644\u0627\u0645\u0629.',
  autoHealDesc:
    '\u062a\u0634\u062e\u064a\u0635 \u0627\u0644\u0623\u0639\u0637\u0627\u0644 \u0648\u062a\u0637\u0628\u064a\u0642 \u0627\u0644\u0625\u0635\u0644\u0627\u062d\u0627\u062a \u0627\u0644\u0630\u0627\u062a\u064a\u0629 \u0639\u0646\u062f \u0627\u0643\u062a\u0634\u0627\u0641 \u0627\u0644\u062e\u0644\u0644.',
  loadBalanceDesc:
    '\u0625\u0639\u0627\u062f\u0629 \u062a\u0648\u0632\u064a\u0639 \u0627\u0644\u062d\u0645\u0644 \u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a\u064b\u0627 \u0639\u0628\u0631 \u0627\u0644\u0648\u0627\u062c\u0647\u0627\u062a \u0648\u0627\u0644\u0645\u0633\u0627\u0631\u0627\u062a.',
  heroTitle: '\u0627\u0644\u0623\u062a\u0645\u062a\u0629 \u0627\u0644\u0630\u0627\u062a\u064a\u0629 \u0627\u0644\u0645\u062f\u0639\u0648\u0645\u0629 \u0628\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0635\u0646\u0627\u0639\u064a',
  heroDescription:
    '\u064a\u062a\u0645 \u062a\u062d\u0644\u064a\u0644 \u0643\u0644 \u0642\u0631\u0627\u0631 \u0628\u0634\u0643\u0644 \u0644\u062d\u0638\u064a \u0642\u0628\u0644 \u0627\u0644\u062a\u0646\u0641\u064a\u0630\u060c \u0645\u0639 \u0627\u0644\u0645\u062d\u0627\u0641\u0638\u0629 \u0639\u0644\u0649 \u0633\u064a\u0627\u0633\u0629 \u0627\u0644\u0623\u0645\u0627\u0646 \u0648\u062a\u0633\u062c\u064a\u0644 \u0643\u0627\u0645\u0644 \u0644\u0643\u0644 \u062e\u0637\u0648\u0629.',
  securityTitle: '\u0633\u064a\u0627\u0633\u0627\u062a \u0627\u0644\u0623\u0645\u0627\u0646 \u0648\u0627\u0644\u0631\u062c\u0648\u0639 \u0627\u0644\u062a\u0644\u0642\u0627\u0626\u064a',
  securityBullet1:
    '\u062a\u0641\u0639\u064a\u0644 snapshot \u0642\u0628\u0644 \u0643\u0644 \u062a\u0646\u0641\u064a\u0630 \u062d\u0631\u062c \u0645\u0639 \u062a\u062e\u0632\u064a\u0646\u0647 \u0641\u064a PostgreSQL \u0648 S3.',
  securityBullet2:
    '\u0625\u0637\u0644\u0627\u0642 \u0642\u0646\u0627\u0629 rollback \u062e\u0644\u0627\u0644 15 \u062b\u0627\u0646\u064a\u0629 \u0641\u064a \u062d\u0627\u0644 \u0627\u0643\u062a\u0634\u0627\u0641 anomaly \u0634\u062f\u064a\u062f\u0629.',
  securityBullet3:
    '\u062a\u0648\u0642\u064a\u0639 \u0631\u0642\u0645\u064a \u0644\u0643\u0644 \u0633\u0643\u0631\u0628\u062a RouterOS \u0642\u0628\u0644 \u0625\u0631\u0633\u0627\u0644\u0647 \u0625\u0644\u0649 \u0627\u0644\u0631\u0627\u0648\u062a\u0631.',
  playbookTitle: '\u062e\u0637\u0629 \u0627\u0644\u062a\u0646\u0641\u064a\u0630 \u0627\u0644\u0645\u062a\u0643\u0631\u0631',
  playbookStep1:
    '\u062a\u062d\u0644\u064a\u0644 \u0627\u0644\u0646\u064a\u0629 \u0639\u0628\u0631 GPT-5\u060c \u062b\u0645 \u0627\u0639\u062a\u0645\u0627\u062f \u0627\u0644\u0646\u062a\u0627\u0626\u062c \u0645\u0646 Gemini.',
  playbookStep2: '\u062a\u0634\u063a\u064a\u0644 Dry-Run \u0645\u0639 \u0645\u062d\u0627\u0643\u0627\u0629 \u0643\u0627\u0645\u0644\u0629 \u0644\u0628\u064a\u0626\u0629 RouterOS.',
  playbookStep3: '\u062a\u0646\u0641\u064a\u0630 \u0641\u0639\u0644\u064a \u0639\u0628\u0631 Executor Engine \u0648\u0645\u0631\u0627\u0642\u0628\u0629 \u0644\u062d\u0638\u064a\u0629 \u0644\u0644\u0623\u062b\u0631.',
  playbookStep4: '\u062a\u0633\u062c\u064a\u0644 \u0634\u0627\u0645\u0644 \u0648\u062a\u062d\u062f\u064a\u062b \u0642\u0627\u0639\u062f\u0629 \u0627\u0644\u0645\u0639\u0631\u0641\u0629 \u062a\u0644\u0642\u0627\u0626\u064a\u064b\u0627.'
};

const toggleDescriptions: Record<string, string> = {
  auto_execute: text.autoExecuteDesc,
  auto_heal: text.autoHealDesc,
  load_balance: text.loadBalanceDesc
};

export function AutomationPage() {
  const [toggles, setToggles] = useState<AutomationToggle[]>([]);

  useEffect(() => {
    const fetchToggles = async () => {
      try {
        const { data } = await api.get<AutomationToggle[]>('/orchestrator/toggles');
        setToggles(data);
      } catch (error) {
        setToggles([
          { feature: 'auto_execute', enabled: false, updated_at: new Date().toISOString() },
          { feature: 'auto_heal', enabled: true, updated_at: new Date().toISOString() },
          { feature: 'load_balance', enabled: true, updated_at: new Date().toISOString() }
        ]);
      }
    };

    fetchToggles();
  }, []);

  const handleToggle = async (feature: string, enabled: boolean) => {
    setToggles((prev) => prev.map((item) => (item.feature === feature ? { ...item, enabled } : item)));
    await api.post(`/orchestrator/toggles/${feature}`, {
      feature,
      enabled,
      updated_at: new Date().toISOString()
    });
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <section className="glass-panel p-6 mb-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <span className="p-4 rounded-3xl bg-gradient-to-br from-neon/30 to-magenta/30">
            <Bot className="w-8 h-8 text-neon" />
          </span>
          <div>
            <h2 className="text-lg font-semibold text-white">{text.heroTitle}</h2>
            <p className="text-sm text-white/60">{text.heroDescription}</p>
          </div>
        </div>
        <Sparkles className="w-6 h-6 text-neon animate-pulse" />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {toggles.map((toggle) => (
          <motion.div
            key={toggle.feature}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`glass-panel p-6 space-y-4 border ${toggle.enabled ? 'border-neon/40' : 'border-white/10'}`}
          >
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-white">{toggle.feature}</h3>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  className="sr-only"
                  checked={toggle.enabled}
                  onChange={(event) => handleToggle(toggle.feature, event.target.checked)}
                />
                <span className="w-12 h-6 bg-black/40 rounded-full peer-focus:outline-none peer-checked:bg-neon/40 flex items-center px-1">
                  <span
                    className={`h-5 w-5 rounded-full bg-white transition-transform ${toggle.enabled ? 'translate-x-6' : ''}`}
                  />
                </span>
              </label>
            </div>
            <p className="text-xs text-white/70 leading-relaxed">{toggleDescriptions[toggle.feature]}</p>
            <p className="text-[10px] text-white/40">
              {'\u0622\u062e\u0631 \u062a\u062d\u062f\u064a\u062b '} {new Date(toggle.updated_at).toLocaleString()}
            </p>
          </motion.div>
        ))}
      </section>

      <section className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass-panel p-6 space-y-4"
        >
          <h3 className="flex items-center gap-2 text-sm text-white/70">
            <ShieldPlus className="w-4 h-4 text-neon" /> {text.securityTitle}
          </h3>
          <ul className="space-y-2 text-xs text-white/70 leading-relaxed list-disc list-inside">
            <li>{text.securityBullet1}</li>
            <li>{text.securityBullet2}</li>
            <li>{text.securityBullet3}</li>
          </ul>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="glass-panel p-6 space-y-4"
        >
          <h3 className="flex items-center gap-2 text-sm text-white/70">
            <Repeat2 className="w-4 h-4 text-magenta" /> {text.playbookTitle}
          </h3>
          <ol className="list-decimal list-inside space-y-2 text-xs text-white/70 leading-relaxed">
            <li>{text.playbookStep1}</li>
            <li>{text.playbookStep2}</li>
            <li>{text.playbookStep3}</li>
            <li>{text.playbookStep4}</li>
          </ol>
        </motion.div>
      </section>
    </motion.div>
  );
}
