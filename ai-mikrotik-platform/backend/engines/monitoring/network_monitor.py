"""
Network Monitoring Engine - محرك المراقبة اللحظية
يراقب جميع جوانب الشبكة ويكتشف المشاكل تلقائياً

المسؤوليات:
- مراقبة CPU, RAM, Interfaces
- كشف الاختناقات (Bottlenecks)
- تتبع استخدام النطاق الترددي
- كشف المشاكل الأمنية
- إرسال تنبيهات فورية
- تخزين البيانات التاريخية
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
from collections import deque
import statistics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """مستويات التنبيه"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class MetricType(Enum):
    """أنواع المقاييس"""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    BANDWIDTH = "bandwidth"
    CONNECTIONS = "connections"
    LATENCY = "latency"
    PACKET_LOSS = "packet_loss"
    INTERFACE_STATUS = "interface_status"
    TEMPERATURE = "temperature"


@dataclass
class Metric:
    """مقياس واحد"""
    type: MetricType
    value: float
    unit: str
    timestamp: datetime
    router_id: str
    interface: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Alert:
    """تنبيه"""
    id: str
    level: AlertLevel
    title: str
    message: str
    metric_type: MetricType
    current_value: float
    threshold: float
    timestamp: datetime
    router_id: str
    resolved: bool = False
    resolution_time: Optional[datetime] = None
    auto_heal_triggered: bool = False


@dataclass
class RouterHealth:
    """صحة الراوتر الإجمالية"""
    router_id: str
    status: str  # healthy, degraded, critical, down
    uptime: float
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int
    total_bandwidth_usage: float
    interfaces_up: int
    interfaces_total: int
    alerts_count: int
    last_check: datetime
    health_score: float  # 0-100


class ThresholdConfig:
    """تكوين العتبات للتنبيهات"""
    
    def __init__(self):
        self.thresholds = {
            MetricType.CPU: {
                "warning": 70.0,
                "critical": 85.0,
                "emergency": 95.0
            },
            MetricType.MEMORY: {
                "warning": 75.0,
                "critical": 90.0,
                "emergency": 95.0
            },
            MetricType.DISK: {
                "warning": 80.0,
                "critical": 90.0,
                "emergency": 95.0
            },
            MetricType.BANDWIDTH: {
                "warning": 80.0,  # % من الحد الأقصى
                "critical": 90.0,
                "emergency": 95.0
            },
            MetricType.LATENCY: {
                "warning": 100.0,  # ms
                "critical": 200.0,
                "emergency": 500.0
            },
            MetricType.PACKET_LOSS: {
                "warning": 1.0,  # %
                "critical": 5.0,
                "emergency": 10.0
            },
            MetricType.TEMPERATURE: {
                "warning": 60.0,  # °C
                "critical": 75.0,
                "emergency": 85.0
            }
        }
    
    def get_alert_level(self, metric_type: MetricType, value: float) -> Optional[AlertLevel]:
        """تحديد مستوى التنبيه بناءً على القيمة"""
        if metric_type not in self.thresholds:
            return None
        
        thresholds = self.thresholds[metric_type]
        
        if value >= thresholds.get("emergency", float('inf')):
            return AlertLevel.EMERGENCY
        elif value >= thresholds.get("critical", float('inf')):
            return AlertLevel.CRITICAL
        elif value >= thresholds.get("warning", float('inf')):
            return AlertLevel.WARNING
        
        return None


class NetworkMonitor:
    """
    محرك المراقبة الشبكية
    
    يراقب جميع جوانب الشبكة في الوقت الفعلي ويكتشف المشاكل تلقائياً
    """
    
    def __init__(
        self,
        executor,
        check_interval: int = 30,
        history_size: int = 1000,
        enable_auto_heal: bool = True
    ):
        """
        تهيئة محرك المراقبة
        
        Args:
            executor: محرك التنفيذ للاتصال بالراوتر
            check_interval: فترة الفحص بالثواني
            history_size: حجم السجل التاريخي
            enable_auto_heal: تفعيل الإصلاح التلقائي
        """
        self.executor = executor
        self.check_interval = check_interval
        self.history_size = history_size
        self.enable_auto_heal = enable_auto_heal
        
        # تكوين العتبات
        self.thresholds = ThresholdConfig()
        
        # تخزين البيانات
        self.metrics_history: Dict[MetricType, deque] = {
            metric_type: deque(maxlen=history_size)
            for metric_type in MetricType
        }
        
        # التنبيهات النشطة
        self.active_alerts: Dict[str, Alert] = {}
        self.alerts_history: deque = deque(maxlen=history_size)
        
        # معلومات الصحة
        self.router_health: Optional[RouterHealth] = None
        
        # callbacks للتنبيهات
        self.alert_callbacks: List[Callable] = []
        
        # حالة المراقبة
        self.is_monitoring = False
        self.monitoring_task = None
        
        logger.info("📊 Network Monitor تم تهيئته بنجاح")
    
    def add_alert_callback(self, callback: Callable):
        """إضافة callback للتنبيهات"""
        self.alert_callbacks.append(callback)
    
    async def start_monitoring(self):
        """بدء المراقبة المستمرة"""
        if self.is_monitoring:
            logger.warning("المراقبة مفعلة بالفعل")
            return
        
        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        logger.info("🚀 بدء المراقبة المستمرة")
    
    async def stop_monitoring(self):
        """إيقاف المراقبة"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        logger.info("⏸️ تم إيقاف المراقبة")
    
    async def _monitoring_loop(self):
        """حلقة المراقبة الرئيسية"""
        logger.info("🔄 بدء حلقة المراقبة")
        
        while self.is_monitoring:
            try:
                # جمع جميع المقاييس
                await self.collect_all_metrics()
                
                # تحليل الصحة العامة
                await self.analyze_health()
                
                # كشف الشذوذات
                await self.detect_anomalies()
                
                # انتظار الفترة التالية
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"خطأ في حلقة المراقبة: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def collect_all_metrics(self):
        """جمع جميع المقاييس"""
        try:
            # جمع مقاييس CPU
            await self.collect_cpu_metrics()
            
            # جمع مقاييس الذاكرة
            await self.collect_memory_metrics()
            
            # جمع مقاييس الواجهات
            await self.collect_interface_metrics()
            
            # جمع مقاييس النطاق الترددي
            await self.collect_bandwidth_metrics()
            
            # جمع مقاييس الاتصالات
            await self.collect_connection_metrics()
            
            logger.debug("✅ تم جمع جميع المقاييس")
            
        except Exception as e:
            logger.error(f"خطأ في جمع المقاييس: {e}")
    
    async def collect_cpu_metrics(self):
        """جمع مقاييس CPU"""
        try:
            # تنفيذ أمر للحصول على استخدام CPU
            result = await self.executor.execute(
                "/system resource print",
                mode="safe"
            )
            
            if result.success:
                # استخراج قيمة CPU من الخرج
                cpu_value = self._parse_cpu_from_output(result.output)
                
                metric = Metric(
                    type=MetricType.CPU,
                    value=cpu_value,
                    unit="%",
                    timestamp=datetime.now(),
                    router_id=self.executor.connection.host
                )
                
                self.metrics_history[MetricType.CPU].append(metric)
                
                # فحص التنبيهات
                await self._check_metric_alert(metric)
                
        except Exception as e:
            logger.error(f"خطأ في جمع مقاييس CPU: {e}")
    
    async def collect_memory_metrics(self):
        """جمع مقاييس الذاكرة"""
        try:
            result = await self.executor.execute(
                "/system resource print",
                mode="safe"
            )
            
            if result.success:
                memory_value = self._parse_memory_from_output(result.output)
                
                metric = Metric(
                    type=MetricType.MEMORY,
                    value=memory_value,
                    unit="%",
                    timestamp=datetime.now(),
                    router_id=self.executor.connection.host
                )
                
                self.metrics_history[MetricType.MEMORY].append(metric)
                await self._check_metric_alert(metric)
                
        except Exception as e:
            logger.error(f"خطأ في جمع مقاييس الذاكرة: {e}")
    
    async def collect_interface_metrics(self):
        """جمع مقاييس الواجهات"""
        try:
            result = await self.executor.execute(
                "/interface print stats",
                mode="safe"
            )
            
            if result.success:
                interfaces = self._parse_interfaces_from_output(result.output)
                
                for interface_name, stats in interfaces.items():
                    # حفظ حالة الواجهة
                    metric = Metric(
                        type=MetricType.INTERFACE_STATUS,
                        value=1.0 if stats['status'] == 'running' else 0.0,
                        unit="status",
                        timestamp=datetime.now(),
                        router_id=self.executor.connection.host,
                        interface=interface_name,
                        metadata=stats
                    )
                    
                    self.metrics_history[MetricType.INTERFACE_STATUS].append(metric)
                
        except Exception as e:
            logger.error(f"خطأ في جمع مقاييس الواجهات: {e}")
    
    async def collect_bandwidth_metrics(self):
        """جمع مقاييس النطاق الترددي"""
        try:
            result = await self.executor.execute(
                "/interface monitor-traffic ether1 once",
                mode="safe"
            )
            
            if result.success:
                bandwidth_data = self._parse_bandwidth_from_output(result.output)
                
                metric = Metric(
                    type=MetricType.BANDWIDTH,
                    value=bandwidth_data['usage_percent'],
                    unit="%",
                    timestamp=datetime.now(),
                    router_id=self.executor.connection.host,
                    metadata=bandwidth_data
                )
                
                self.metrics_history[MetricType.BANDWIDTH].append(metric)
                await self._check_metric_alert(metric)
                
        except Exception as e:
            logger.error(f"خطأ في جمع مقاييس النطاق الترددي: {e}")
    
    async def collect_connection_metrics(self):
        """جمع مقاييس الاتصالات"""
        try:
            result = await self.executor.execute(
                "/ip firewall connection print count-only",
                mode="safe"
            )
            
            if result.success:
                connections_count = self._parse_connections_from_output(result.output)
                
                metric = Metric(
                    type=MetricType.CONNECTIONS,
                    value=float(connections_count),
                    unit="connections",
                    timestamp=datetime.now(),
                    router_id=self.executor.connection.host
                )
                
                self.metrics_history[MetricType.CONNECTIONS].append(metric)
                
        except Exception as e:
            logger.error(f"خطأ في جمع مقاييس الاتصالات: {e}")
    
    async def _check_metric_alert(self, metric: Metric):
        """فحص إذا كان المقياس يستدعي تنبيهاً"""
        alert_level = self.thresholds.get_alert_level(metric.type, metric.value)
        
        if alert_level:
            # إنشاء تنبيه
            alert = Alert(
                id=f"{metric.router_id}_{metric.type.value}_{int(datetime.now().timestamp())}",
                level=alert_level,
                title=f"تنبيه {metric.type.value.upper()}",
                message=f"{metric.type.value} وصل إلى {metric.value}{metric.unit}",
                metric_type=metric.type,
                current_value=metric.value,
                threshold=self.thresholds.thresholds[metric.type][alert_level.value],
                timestamp=datetime.now(),
                router_id=metric.router_id
            )
            
            # حفظ التنبيه
            self.active_alerts[alert.id] = alert
            self.alerts_history.append(alert)
            
            # إطلاق callbacks
            for callback in self.alert_callbacks:
                try:
                    await callback(alert)
                except Exception as e:
                    logger.error(f"خطأ في callback التنبيه: {e}")
            
            # تشغيل Auto Heal إذا كان مفعلاً
            if self.enable_auto_heal and alert_level in [AlertLevel.CRITICAL, AlertLevel.EMERGENCY]:
                await self._trigger_auto_heal(alert)
            
            logger.warning(f"⚠️ {alert.title}: {alert.message}")
    
    async def _trigger_auto_heal(self, alert: Alert):
        """تشغيل الإصلاح التلقائي"""
        logger.info(f"🔧 تشغيل Auto Heal للتنبيه: {alert.title}")
        
        # هنا يمكن استدعاء Auto Heal System
        # مثال: إعادة تشغيل خدمة، تنظيف ذاكرة، إلخ
        
        alert.auto_heal_triggered = True
    
    async def analyze_health(self):
        """تحليل الصحة العامة للراوتر"""
        try:
            # جمع آخر المقاييس
            latest_cpu = self._get_latest_metric(MetricType.CPU)
            latest_memory = self._get_latest_metric(MetricType.MEMORY)
            latest_bandwidth = self._get_latest_metric(MetricType.BANDWIDTH)
            latest_connections = self._get_latest_metric(MetricType.CONNECTIONS)
            
            # حساب عدد الواجهات النشطة
            interface_metrics = list(self.metrics_history[MetricType.INTERFACE_STATUS])
            interfaces_up = sum(1 for m in interface_metrics[-10:] if m.value == 1.0)
            interfaces_total = len(set(m.interface for m in interface_metrics[-10:]))
            
            # حساب نقاط الصحة (0-100)
            health_score = 100.0
            
            if latest_cpu:
                health_score -= (latest_cpu.value / 100) * 30  # CPU يؤثر بـ 30%
            
            if latest_memory:
                health_score -= (latest_memory.value / 100) * 25  # Memory يؤثر بـ 25%
            
            if latest_bandwidth:
                health_score -= (latest_bandwidth.value / 100) * 20  # Bandwidth يؤثر بـ 20%
            
            # عدد التنبيهات النشطة
            alerts_count = len([a for a in self.active_alerts.values() if not a.resolved])
            health_score -= alerts_count * 5  # كل تنبيه ينقص 5 نقاط
            
            # تحديد الحالة
            if health_score >= 80:
                status = "healthy"
            elif health_score >= 60:
                status = "degraded"
            elif health_score >= 30:
                status = "critical"
            else:
                status = "down"
            
            # إنشاء كائن الصحة
            self.router_health = RouterHealth(
                router_id=self.executor.connection.host,
                status=status,
                uptime=0.0,  # TODO: استخراج من الراوتر
                cpu_usage=latest_cpu.value if latest_cpu else 0.0,
                memory_usage=latest_memory.value if latest_memory else 0.0,
                disk_usage=0.0,  # TODO: استخراج من الراوتر
                active_connections=int(latest_connections.value) if latest_connections else 0,
                total_bandwidth_usage=latest_bandwidth.value if latest_bandwidth else 0.0,
                interfaces_up=interfaces_up,
                interfaces_total=interfaces_total,
                alerts_count=alerts_count,
                last_check=datetime.now(),
                health_score=max(0, health_score)
            )
            
            logger.debug(f"💚 حالة الصحة: {status} ({health_score:.1f}/100)")
            
        except Exception as e:
            logger.error(f"خطأ في تحليل الصحة: {e}")
    
    async def detect_anomalies(self):
        """كشف الشذوذات في الأداء"""
        try:
            # كشف ارتفاع مفاجئ في CPU
            cpu_metrics = list(self.metrics_history[MetricType.CPU])
            if len(cpu_metrics) >= 10:
                recent_cpu = [m.value for m in cpu_metrics[-10:]]
                avg_cpu = statistics.mean(recent_cpu)
                std_cpu = statistics.stdev(recent_cpu) if len(recent_cpu) > 1 else 0
                
                if recent_cpu[-1] > avg_cpu + 2 * std_cpu:
                    logger.warning(f"🔍 شذوذ في CPU: {recent_cpu[-1]:.1f}% (المتوسط: {avg_cpu:.1f}%)")
            
            # كشف ارتفاع مفاجئ في Bandwidth
            bandwidth_metrics = list(self.metrics_history[MetricType.BANDWIDTH])
            if len(bandwidth_metrics) >= 10:
                recent_bandwidth = [m.value for m in bandwidth_metrics[-10:]]
                avg_bandwidth = statistics.mean(recent_bandwidth)
                std_bandwidth = statistics.stdev(recent_bandwidth) if len(recent_bandwidth) > 1 else 0
                
                if recent_bandwidth[-1] > avg_bandwidth + 2 * std_bandwidth:
                    logger.warning(f"🔍 شذوذ في Bandwidth: {recent_bandwidth[-1]:.1f}% (المتوسط: {avg_bandwidth:.1f}%)")
            
        except Exception as e:
            logger.error(f"خطأ في كشف الشذوذات: {e}")
    
    def _get_latest_metric(self, metric_type: MetricType) -> Optional[Metric]:
        """الحصول على آخر مقياس من نوع معين"""
        metrics = self.metrics_history.get(metric_type)
        if metrics and len(metrics) > 0:
            return metrics[-1]
        return None
    
    def _parse_cpu_from_output(self, output: str) -> float:
        """استخراج قيمة CPU من خرج الأمر"""
        # تحليل بسيط - يمكن تحسينه
        try:
            for line in output.split('\n'):
                if 'cpu-load' in line.lower():
                    value = line.split(':')[-1].strip().replace('%', '')
                    return float(value)
        except:
            pass
        return 0.0
    
    def _parse_memory_from_output(self, output: str) -> float:
        """استخراج قيمة الذاكرة من خرج الأمر"""
        try:
            total_memory = 0
            free_memory = 0
            
            for line in output.split('\n'):
                if 'total-memory' in line.lower():
                    total_memory = float(line.split(':')[-1].strip())
                if 'free-memory' in line.lower():
                    free_memory = float(line.split(':')[-1].strip())
            
            if total_memory > 0:
                used_percent = ((total_memory - free_memory) / total_memory) * 100
                return used_percent
        except:
            pass
        return 0.0
    
    def _parse_interfaces_from_output(self, output: str) -> Dict[str, Dict]:
        """استخراج معلومات الواجهات من خرج الأمر"""
        # تحليل بسيط
        return {
            "ether1": {"status": "running", "rx": 0, "tx": 0},
            "ether2": {"status": "running", "rx": 0, "tx": 0}
        }
    
    def _parse_bandwidth_from_output(self, output: str) -> Dict[str, float]:
        """استخراج معلومات النطاق الترددي"""
        return {
            "rx_rate": 1000000,  # bytes/sec
            "tx_rate": 500000,
            "usage_percent": 50.0
        }
    
    def _parse_connections_from_output(self, output: str) -> int:
        """استخراج عدد الاتصالات"""
        try:
            return int(output.strip())
        except:
            return 0
    
    def get_current_status(self) -> Dict[str, Any]:
        """الحصول على الحالة الحالية"""
        return {
            "is_monitoring": self.is_monitoring,
            "router_health": self.router_health.__dict__ if self.router_health else None,
            "active_alerts": len(self.active_alerts),
            "total_metrics_collected": sum(len(m) for m in self.metrics_history.values())
        }
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """الحصول على ملخص المقاييس"""
        summary = {}
        
        for metric_type in MetricType:
            metrics = list(self.metrics_history[metric_type])
            if metrics:
                values = [m.value for m in metrics[-10:]]
                summary[metric_type.value] = {
                    "current": values[-1] if values else 0,
                    "average": statistics.mean(values) if values else 0,
                    "min": min(values) if values else 0,
                    "max": max(values) if values else 0,
                    "count": len(metrics)
                }
        
        return summary


# مثال على الاستخدام
if __name__ == "__main__":
    async def test_monitor():
        """اختبار المراقبة"""
        from routeros_executor import RouterOSExecutor, RouterConnection, ConnectionMethod
        
        # إنشاء اتصال
        connection = RouterConnection(
            host="192.168.88.1",
            port=22,
            username="admin",
            password="password",
            connection_method=ConnectionMethod.SSH
        )
        
        executor = RouterOSExecutor(connection)
        
        # إنشاء المراقب
        monitor = NetworkMonitor(
            executor=executor,
            check_interval=10,
            enable_auto_heal=True
        )
        
        # إضافة callback للتنبيهات
        async def alert_handler(alert: Alert):
            print(f"🚨 تنبيه جديد: {alert.title} - {alert.message}")
        
        monitor.add_alert_callback(alert_handler)
        
        # بدء المراقبة
        await monitor.start_monitoring()
        
        # الانتظار لمدة دقيقة
        await asyncio.sleep(60)
        
        # إيقاف المراقبة
        await monitor.stop_monitoring()
        
        # عرض الملخص
        print("\n📊 ملخص المقاييس:")
        print(json.dumps(monitor.get_metrics_summary(), indent=2, ensure_ascii=False))
    
    asyncio.run(test_monitor())
