"""
Auto-Heal System - النظام الذاتي للإصلاح
يكتشف المشاكل ويصلحها تلقائياً بدون تدخل بشري

المسؤوليات:
- كشف الأخطاء والمشاكل الشائعة
- تشخيص المشكلة وتحديد الحل الأمثل
- تنفيذ الإصلاح التلقائي
- التحقق من نجاح الإصلاح
- التعلم من محاولات الإصلاح السابقة
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IssueType(Enum):
    """أنواع المشاكل القابلة للإصلاح"""
    HIGH_CPU = "high_cpu"
    HIGH_MEMORY = "high_memory"
    HIGH_BANDWIDTH = "high_bandwidth"
    INTERFACE_DOWN = "interface_down"
    CONNECTION_OVERLOAD = "connection_overload"
    FIREWALL_ISSUE = "firewall_issue"
    DNS_ISSUE = "dns_issue"
    DHCP_ISSUE = "dhcp_issue"
    ROUTING_ISSUE = "routing_issue"


class HealingStatus(Enum):
    """حالة عملية الإصلاح"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class HealingAttempt:
    """محاولة إصلاح"""
    id: str
    issue_type: IssueType
    detected_at: datetime
    description: str
    solution_applied: str
    status: HealingStatus
    execution_time: float
    before_metrics: Dict
    after_metrics: Optional[Dict]
    error: Optional[str]


class AutoHealSystem:
    """
    النظام الذاتي للإصلاح - Auto-Heal System
    
    يكتشف المشاكل تلقائياً ويطبق الحلول المناسبة
    """
    
    def __init__(
        self,
        executor,
        monitor,
        ai_brain,
        max_attempts: int = 3,
        cooldown_period: int = 300,  # 5 دقائق
        enabled: bool = True
    ):
        """
        تهيئة نظام الإصلاح الذاتي
        
        Args:
            executor: محرك التنفيذ
            monitor: محرك المراقبة
            ai_brain: العقل الصناعي
            max_attempts: أقصى عدد محاولات للإصلاح
            cooldown_period: فترة الانتظار بين المحاولات (بالثواني)
            enabled: تفعيل/تعطيل النظام
        """
        self.executor = executor
        self.monitor = monitor
        self.ai_brain = ai_brain
        self.max_attempts = max_attempts
        self.cooldown_period = cooldown_period
        self.enabled = enabled
        
        # سجل محاولات الإصلاح
        self.healing_history: List[HealingAttempt] = []
        
        # عداد المحاولات لكل نوع مشكلة
        self.attempt_counters: Dict[IssueType, int] = {}
        
        # وقت آخر محاولة لكل نوع
        self.last_attempt_time: Dict[IssueType, datetime] = {}
        
        # قاعدة حلول معروفة
        self.known_solutions = self._initialize_known_solutions()
        
        logger.info("🔧 Auto-Heal System تم تهيئته بنجاح")
    
    def _initialize_known_solutions(self) -> Dict[IssueType, List[str]]:
        """تهيئة قاعدة الحلول المعروفة"""
        return {
            IssueType.HIGH_CPU: [
                "تنظيف جدول الاتصالات القديمة",
                "إعادة تشغيل الخدمات غير الضرورية",
                "تحسين قواعد Firewall",
                "تقليل Logging"
            ],
            IssueType.HIGH_MEMORY: [
                "تنظيف الذاكرة المؤقتة",
                "إعادة تشغيل الخدمات",
                "تقليل Connection Tracking",
                "إزالة ملفات Log القديمة"
            ],
            IssueType.HIGH_BANDWIDTH: [
                "تفعيل Queue Tree",
                "تحديد سرعة للمستخدمين المفرطين",
                "تفعيل Traffic Shaping",
                "حجب التورنت مؤقتاً"
            ],
            IssueType.INTERFACE_DOWN: [
                "إعادة تشغيل الواجهة",
                "فحص الكابل",
                "إعادة ضبط الإعدادات",
                "التبديل إلى واجهة احتياطية"
            ],
            IssueType.CONNECTION_OVERLOAD: [
                "زيادة حد Connection Tracking",
                "تنظيف الاتصالات القديمة",
                "تفعيل SYN Flood Protection",
                "حظر IPs المشبوهة"
            ]
        }
    
    async def analyze_and_heal(self, alert) -> Optional[HealingAttempt]:
        """
        تحليل التنبيه ومحاولة الإصلاح
        
        Args:
            alert: التنبيه المراد معالجته
            
        Returns:
            محاولة الإصلاح
        """
        if not self.enabled:
            logger.info("⏸️ Auto-Heal معطل")
            return None
        
        # تحديد نوع المشكلة
        issue_type = self._identify_issue_type(alert)
        if not issue_type:
            logger.warning(f"❓ لا يمكن تحديد نوع المشكلة من التنبيه: {alert.title}")
            return None
        
        # التحقق من الـ cooldown
        if not self._check_cooldown(issue_type):
            logger.info(f"⏳ في فترة cooldown لـ {issue_type.value}")
            return None
        
        # التحقق من عدد المحاولات
        if not self._check_max_attempts(issue_type):
            logger.warning(f"❌ تم تجاوز الحد الأقصى للمحاولات لـ {issue_type.value}")
            return None
        
        # جمع المقاييس قبل الإصلاح
        before_metrics = await self._collect_metrics()
        
        logger.info(f"🔍 تحليل المشكلة: {issue_type.value}")
        
        # الحصول على الحل من الذكاء الصناعي
        solution = await self._get_ai_solution(alert, issue_type, before_metrics)
        
        if not solution:
            logger.error(f"❌ لا يوجد حل متاح لـ {issue_type.value}")
            return None
        
        # إنشاء محاولة إصلاح
        attempt = HealingAttempt(
            id=f"heal-{datetime.now().timestamp()}",
            issue_type=issue_type,
            detected_at=datetime.now(),
            description=alert.message,
            solution_applied=solution['script'],
            status=HealingStatus.IN_PROGRESS,
            execution_time=0,
            before_metrics=before_metrics,
            after_metrics=None,
            error=None
        )
        
        try:
            # تنفيذ الحل
            logger.info(f"⚡ تطبيق الحل: {solution['description']}")
            
            start_time = datetime.now()
            result = await self.executor.execute(
                script=solution['script'],
                mode="safe",
                description=f"Auto-Heal: {issue_type.value}"
            )
            execution_time = (datetime.now() - start_time).total_seconds()
            
            if result.success:
                # انتظار لمدة قصيرة ثم جمع المقاييس الجديدة
                await asyncio.sleep(10)
                after_metrics = await self._collect_metrics()
                
                # التحقق من نجاح الإصلاح
                if self._verify_healing(issue_type, before_metrics, after_metrics):
                    attempt.status = HealingStatus.SUCCESS
                    attempt.after_metrics = after_metrics
                    attempt.execution_time = execution_time
                    
                    logger.info(f"✅ تم الإصلاح بنجاح: {issue_type.value}")
                    
                    # إعادة تعيين العداد
                    self.attempt_counters[issue_type] = 0
                else:
                    attempt.status = HealingStatus.FAILED
                    attempt.error = "لم يتم حل المشكلة بعد التطبيق"
                    
                    logger.warning(f"⚠️ لم يتم حل المشكلة: {issue_type.value}")
            else:
                attempt.status = HealingStatus.FAILED
                attempt.error = result.error
                
                logger.error(f"❌ فشل تنفيذ الحل: {result.error}")
        
        except Exception as e:
            attempt.status = HealingStatus.FAILED
            attempt.error = str(e)
            
            logger.error(f"❌ خطأ في الإصلاح: {e}")
        
        # تحديث السجلات
        self.healing_history.append(attempt)
        self.last_attempt_time[issue_type] = datetime.now()
        self.attempt_counters[issue_type] = self.attempt_counters.get(issue_type, 0) + 1
        
        return attempt
    
    def _identify_issue_type(self, alert) -> Optional[IssueType]:
        """تحديد نوع المشكلة من التنبيه"""
        metric_type = alert.metric_type.value
        
        mapping = {
            "cpu": IssueType.HIGH_CPU,
            "memory": IssueType.HIGH_MEMORY,
            "bandwidth": IssueType.HIGH_BANDWIDTH,
            "interface_status": IssueType.INTERFACE_DOWN,
            "connections": IssueType.CONNECTION_OVERLOAD
        }
        
        return mapping.get(metric_type)
    
    def _check_cooldown(self, issue_type: IssueType) -> bool:
        """التحقق من فترة الانتظار"""
        if issue_type not in self.last_attempt_time:
            return True
        
        last_attempt = self.last_attempt_time[issue_type]
        cooldown_end = last_attempt + timedelta(seconds=self.cooldown_period)
        
        return datetime.now() > cooldown_end
    
    def _check_max_attempts(self, issue_type: IssueType) -> bool:
        """التحقق من عدد المحاولات"""
        attempts = self.attempt_counters.get(issue_type, 0)
        return attempts < self.max_attempts
    
    async def _collect_metrics(self) -> Dict:
        """جمع المقاييس الحالية"""
        if self.monitor and self.monitor.router_health:
            return {
                "cpu_usage": self.monitor.router_health.cpu_usage,
                "memory_usage": self.monitor.router_health.memory_usage,
                "active_connections": self.monitor.router_health.active_connections,
                "health_score": self.monitor.router_health.health_score
            }
        return {}
    
    async def _get_ai_solution(
        self,
        alert,
        issue_type: IssueType,
        metrics: Dict
    ) -> Optional[Dict]:
        """الحصول على حل من الذكاء الصناعي"""
        try:
            # بناء رسالة للذكاء الصناعي
            message = f"""
            المشكلة: {issue_type.value}
            التفاصيل: {alert.message}
            المقاييس الحالية: {metrics}
            
            قدم حلاً سريعاً وفعالاً بسكربت MikroTik RouterOS.
            """
            
            # استخدام الذكاء الصناعي
            decision = await self.ai_brain.process_natural_language(
                user_message=message,
                network_context=None,
                user_role="auto_heal_system"
            )
            
            if decision.mikrotik_script:
                return {
                    "description": decision.reasoning,
                    "script": decision.mikrotik_script,
                    "confidence": decision.confidence
                }
            
            # إذا لم يتمكن الذكاء الصناعي، استخدم الحلول المعروفة
            return self._get_known_solution(issue_type)
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على حل AI: {e}")
            return self._get_known_solution(issue_type)
    
    def _get_known_solution(self, issue_type: IssueType) -> Optional[Dict]:
        """الحصول على حل من قاعدة الحلول المعروفة"""
        solutions = self.known_solutions.get(issue_type, [])
        
        if not solutions:
            return None
        
        # اختيار أول حل (يمكن تحسينه بالتعلم)
        description = solutions[0]
        
        # توليد سكربت بسيط بناءً على الحل
        script = self._generate_basic_script(issue_type, description)
        
        return {
            "description": description,
            "script": script,
            "confidence": 0.7
        }
    
    def _generate_basic_script(self, issue_type: IssueType, description: str) -> str:
        """توليد سكربت أساسي"""
        scripts = {
            IssueType.HIGH_CPU: "/system resource cpu print; /log print where topics~\"system,error,critical\"",
            IssueType.HIGH_MEMORY: "/system resource print; /log print",
            IssueType.HIGH_BANDWIDTH: "/interface print stats",
            IssueType.INTERFACE_DOWN: "/interface print; /interface enable [find disabled=yes]",
            IssueType.CONNECTION_OVERLOAD: "/ip firewall connection print count-only"
        }
        
        return scripts.get(issue_type, "/system resource print")
    
    def _verify_healing(
        self,
        issue_type: IssueType,
        before: Dict,
        after: Dict
    ) -> bool:
        """التحقق من نجاح الإصلاح"""
        if not before or not after:
            return False
        
        # قواعد التحقق حسب نوع المشكلة
        if issue_type == IssueType.HIGH_CPU:
            return after.get("cpu_usage", 100) < before.get("cpu_usage", 100) - 10
        
        elif issue_type == IssueType.HIGH_MEMORY:
            return after.get("memory_usage", 100) < before.get("memory_usage", 100) - 10
        
        elif issue_type == IssueType.CONNECTION_OVERLOAD:
            return after.get("active_connections", 0) < before.get("active_connections", 999999)
        
        # افتراضياً: تحسن في health_score
        return after.get("health_score", 0) > before.get("health_score", 0)
    
    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات النظام"""
        total_attempts = len(self.healing_history)
        successful = len([a for a in self.healing_history if a.status == HealingStatus.SUCCESS])
        failed = len([a for a in self.healing_history if a.status == HealingStatus.FAILED])
        
        return {
            "enabled": self.enabled,
            "total_attempts": total_attempts,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_attempts * 100) if total_attempts > 0 else 0,
            "recent_attempts": [
                {
                    "issue_type": a.issue_type.value,
                    "status": a.status.value,
                    "detected_at": a.detected_at.isoformat(),
                    "execution_time": a.execution_time
                }
                for a in self.healing_history[-10:]
            ]
        }


# مثال على الاستخدام
if __name__ == "__main__":
    async def test_auto_heal():
        """اختبار نظام الإصلاح الذاتي"""
        from routeros_executor import RouterOSExecutor, RouterConnection, ConnectionMethod
        from network_monitor import NetworkMonitor
        from core_ai_brain import CoreAIBrain
        
        # إنشاء المكونات
        connection = RouterConnection(
            host="192.168.88.1",
            port=22,
            username="admin",
            password="password",
            connection_method=ConnectionMethod.SSH
        )
        
        executor = RouterOSExecutor(connection)
        await executor.connect()
        
        monitor = NetworkMonitor(executor, check_interval=30)
        
        ai_brain = CoreAIBrain(
            openai_api_key="your-key",
            gemini_api_key="your-key"
        )
        
        # إنشاء نظام الإصلاح الذاتي
        auto_heal = AutoHealSystem(
            executor=executor,
            monitor=monitor,
            ai_brain=ai_brain,
            max_attempts=3,
            cooldown_period=60,
            enabled=True
        )
        
        # عرض الإحصائيات
        stats = auto_heal.get_statistics()
        print("📊 إحصائيات Auto-Heal:")
        print(f"إجمالي المحاولات: {stats['total_attempts']}")
        print(f"الناجحة: {stats['successful']}")
        print(f"الفاشلة: {stats['failed']}")
        print(f"نسبة النجاح: {stats['success_rate']:.1f}%")
    
    asyncio.run(test_auto_heal())
