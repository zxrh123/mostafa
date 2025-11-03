import { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { Activity, Cpu, GaugeCircle, Network, Wifi } from 'lucide-react';

import { MetricCard } from '../components/MetricCard';
import { RealtimeTrend } from '../components/RealtimeTrend';
import { NotificationFeed } from '../components/NotificationFeed';
import { AIChatWidget } from '../components/AIChatWidget';
import { fetchMonitoringSnapshot } from '../lib/api';

interface SnapshotDevice {
  host: string;
  cpu_load: number;
  memory_usage: number;
  uptime: number;
  active_users: number;
  packet_loss: number;
  latency: number;
}

interface SnapshotResponse {
  devices: SnapshotDevice[];
  anomalies: string[];
}

const fallbackSnapshot: SnapshotResponse = {
  devices: [
    {
      host: '10.0.0.1',
      cpu_load: 35.2,
      memory_usage: 48.7,
      uptime: 523000,
      active_users: 241,
      packet_loss: 0.8,
      latency: 12
    }
  ],
  anomalies: []
};

const text = {
  notifTitle1: '\u062a\u062d\u0633\u064a\u0646 \u0627\u0644\u0637\u0627\u0628\u0648\u0631 \u0627\u0644\u062f\u064a\u0646\u0627\u0645\u064a\u0643\u064a',
  notifMessage1:
    '\u062a\u0645 \u0625\u0639\u0627\u062f\u0629 \u062a\u0648\u0632\u064a\u0639 \u0627\u0644\u062d\u0645\u0644 \u0639\u0644\u0649 ether1 \u0648 ether2 \u0644\u062a\u0642\u0644\u064a\u0644 \u0627\u0644\u062a\u0623\u062e\u064a\u0631 \u0628\u0646\u0633\u0628\u0629 18%.',
  notifTime1: '\u0642\u0628\u0644 \u062f\u0642\u064a\u0642\u0629',
  notifTitle2: '\u0627\u062d\u062a\u0645\u0627\u0644 \u0627\u062e\u062a\u0646\u0627\u0642 \u062a\u062d\u0645\u064a\u0644',
  notifMessage2:
    '\u0648\u0627\u062c\u0647\u0629 wlan1 \u0627\u0642\u062a\u0631\u0628\u062a \u0645\u0646 92% \u0645\u0646 \u0627\u0644\u0633\u0639\u0629 \u0627\u0644\u0642\u0635\u0648\u0649. \u0627\u0642\u062a\u0631\u0627\u062d: \u062a\u0648\u0633\u064a\u0639 \u0627\u0644\u0642\u0646\u0627\u0629 \u0623\u0648 \u062a\u0645\u0643\u064a\u0646 5GHz \u0627\u0644\u0625\u0636\u0627\u0641\u064a\u0629.',
  notifTime2: '\u0642\u0628\u0644 3 \u062f\u0642\u0627\u0626\u0642',
  notifTitle3: '\u0627\u0634\u062a\u0628\u0647 \u0628\u0633\u0644\u0648\u0643 \u062f\u062e\u0648\u0644 \u063a\u064a\u0631 \u0637\u0628\u064a\u0639\u064a',
  notifMessage3:
    '\u0645\u062d\u0627\u0648\u0644\u0629 \u062a\u0633\u062c\u064a\u0644 \u062f\u062e\u0648\u0644 \u0645\u062a\u0643\u0631\u0631 \u0645\u0646 41.215.22.10 - \u062a\u0645 \u062a\u0641\u0639\u064a\u0644 \u0627\u0644\u062f\u0641\u0627\u0639 \u0627\u0644\u062a\u0644\u0642\u0627\u0626\u064a.',
  notifTime3: '\u0642\u0628\u0644 7 \u062f\u0642\u0627\u0626\u0642',
  metricCpuTitle: '\u0645\u062a\u0648\u0633\u0637 \u0627\u0633\u062a\u0647\u0644\u0627\u0643 CPU',
  metricCpuSubtitle: '\u062a\u062d\u0644\u064a\u0644 \u0644\u062d\u0638\u064a \u0644\u0643\u0644 \u0627\u0644\u0631\u0627\u0648\u062a\u0631\u0627\u062a',
  metricUsersTitle: '\u0627\u0644\u0639\u0645\u0644\u0627\u0621 \u0627\u0644\u0646\u0634\u0637\u0648\u0646',
  metricUsersSubtitle: '\u062a\u0645 \u0627\u0644\u062a\u0639\u0631\u0641 \u0639\u0644\u0649 \u0633\u0644\u0648\u0643 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646 \u0648\u062a\u0648\u0632\u064a\u0639\u0647\u0645',
  metricLossTitle: '\u0641\u0642\u062f\u0627\u0646 \u0627\u0644\u062d\u0632\u0645',
  metricLossSubtitle: '\u064a\u062a\u0645 \u062a\u0637\u0628\u064a\u0642 \u0622\u0644\u064a\u0627\u062a \u0625\u0635\u0644\u0627\u062d \u062a\u0644\u0642\u0627\u0626\u064a \u0639\u0646\u062f \u0627\u0644\u062d\u0627\u062c\u0629',
  metricLatencyTitle: '\u0632\u0645\u0646 \u0627\u0644\u0627\u0633\u062a\u062c\u0627\u0628\u0629',
  metricLatencySubtitle: '\u064a\u062a\u0645 \u062a\u0648\u062c\u064a\u0647 \u0627\u0644\u0645\u0633\u0627\u0631\u0627\u062a \u0627\u0644\u0630\u0643\u064a\u0629 \u0639\u0628\u0631 \u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0635\u0646\u0627\u0639\u064a',
  trendLatency: '\u0632\u0645\u0646 \u0627\u0644\u0627\u0633\u062a\u062c\u0627\u0628\u0629 \u0627\u0644\u0644\u062d\u0638\u064a',
  trendCpu: '\u062a\u062d\u0645\u064a\u0644 \u0648\u062d\u062f\u0629 \u0627\u0644\u0645\u0639\u0627\u0644\u062c\u0629',
  overviewTitle: '\u0646\u0638\u0631\u0629 \u0639\u0627\u0645\u0629 \u0639\u0644\u0649 \u0627\u0644\u0634\u0628\u0643\u0629',
  overviewAvgCpu: '\u0645\u062a\u0648\u0633\u0637 \u0627\u0644\u0645\u0639\u0627\u0644\u062c',
  overviewNetworkActivity: '\u0646\u0634\u0627\u0637 \u0627\u0644\u0634\u0628\u0643\u0629',
  overviewPacketLoss: '\u0641\u0642\u062f\u0627\u0646 \u0627\u0644\u062d\u0632\u0645',
  overviewLatency: '\u0627\u0644\u0632\u0645\u0646',
  overviewActiveUsersSuffix: '\u0645\u0633\u062a\u062e\u062f\u0645'
};

const notificationSamples = [
  {
    id: '1',
    title: text.notifTitle1,
    message: text.notifMessage1,
    severity: 'info' as const,
    timestamp: text.notifTime1
  },
  {
    id: '2',
    title: text.notifTitle2,
    message: text.notifMessage2,
    severity: 'warning' as const,
    timestamp: text.notifTime2
  },
  {
    id: '3',
    title: text.notifTitle3,
    message: text.notifMessage3,
    severity: 'critical' as const,
    timestamp: text.notifTime3
  }
];

export function DashboardPage() {
  const [snapshot, setSnapshot] = useState<SnapshotResponse>(fallbackSnapshot);
  const [latencySeries, setLatencySeries] = useState<number[]>([12, 10, 14, 11, 13]);
  const [cpuSeries, setCpuSeries] = useState<number[]>([40, 42, 39, 44, 38]);

  useEffect(() => {
    const loadSnapshot = async () => {
      try {
        const response = await fetchMonitoringSnapshot();
        setSnapshot(response);
        if (response.devices.length > 0) {
          setLatencySeries((prev) => [...prev.slice(-9), response.devices[0].latency]);
          setCpuSeries((prev) => [...prev.slice(-9), response.devices[0].cpu_load]);
        }
      } catch (error) {
        // keep fallback data
      }
    };

    loadSnapshot();
    const interval = setInterval(loadSnapshot, 15_000);
    return () => clearInterval(interval);
  }, []);

  const primaryDevice = useMemo(() => snapshot.devices[0], [snapshot.devices]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="space-y-8"
    >
      <section className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
        <MetricCard
          title={text.metricCpuTitle}
          value={`${primaryDevice?.cpu_load.toFixed(1) ?? '--'}%`}
          subtitle={text.metricCpuSubtitle}
          trend={primaryDevice?.cpu_load && primaryDevice.cpu_load < 65 ? 'stable' : 'up'}
        />
        <MetricCard
          title={text.metricUsersTitle}
          value={`${primaryDevice?.active_users ?? '--'}`}
          subtitle={text.metricUsersSubtitle}
          trend="up"
        />
        <MetricCard
          title={text.metricLossTitle}
          value={`${primaryDevice?.packet_loss.toFixed(2) ?? '--'}%`}
          subtitle={text.metricLossSubtitle}
          trend={primaryDevice && primaryDevice.packet_loss > 2 ? 'up' : 'stable'}
        />
        <MetricCard
          title={text.metricLatencyTitle}
          value={`${primaryDevice?.latency.toFixed(1) ?? '--'} ms`}
          subtitle={text.metricLatencySubtitle}
          trend="down"
        />
      </section>

      <section className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 space-y-6">
          <RealtimeTrend title={text.trendLatency} data={latencySeries} unit="ms" />
          <RealtimeTrend title={text.trendCpu} data={cpuSeries} unit="%" />
        </div>
        <div className="h-[32rem]">
          <NotificationFeed items={notificationSamples} />
        </div>
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AIChatWidget />
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          className="glass-panel p-6 space-y-4"
        >
          <h3 className="text-sm text-white/70 flex items-center gap-2">
            <GaugeCircle className="w-4 h-4 text-neon" /> {text.overviewTitle}
          </h3>
          <div className="grid grid-cols-2 gap-4 text-sm text-white/70">
            <div className="flex items-center gap-3 bg-black/30 rounded-2xl px-4 py-3">
              <Cpu className="w-5 h-5 text-neon" />
              <div>
                <p>{text.overviewAvgCpu}</p>
                <p className="text-white font-semibold">{primaryDevice?.cpu_load.toFixed(1) ?? '--'}%</p>
              </div>
            </div>
            <div className="flex items-center gap-3 bg-black/30 rounded-2xl px-4 py-3">
              <Activity className="w-5 h-5 text-magenta" />
              <div>
                <p>{text.overviewNetworkActivity}</p>
                <p className="text-white font-semibold">
                  {primaryDevice?.active_users ?? '--'} {text.overviewActiveUsersSuffix}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3 bg-black/30 rounded-2xl px-4 py-3">
              <Wifi className="w-5 h-5 text-neon" />
              <div>
                <p>{text.overviewPacketLoss}</p>
                <p className="text-white font-semibold">{primaryDevice?.packet_loss.toFixed(2) ?? '--'}%</p>
              </div>
            </div>
            <div className="flex items-center gap-3 bg-black/30 rounded-2xl px-4 py-3">
              <Network className="w-5 h-5 text-magenta" />
              <div>
                <p>{text.overviewLatency}</p>
                <p className="text-white font-semibold">{primaryDevice?.latency.toFixed(1) ?? '--'} ms</p>
              </div>
            </div>
          </div>
        </motion.div>
      </section>
    </motion.div>
  );
}
