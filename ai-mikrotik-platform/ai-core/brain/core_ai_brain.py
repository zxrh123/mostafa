"""
Core AI Brain - العقل الصناعي المركزي
هذا هو العقل الرئيسي للنظام بأكمله - يحلل، يقرر، ينفذ، ويتعلم

المسؤوليات:
- تحليل اللغة الطبيعية وفهم النية (Intent Recognition)
- التواصل مع GPT-5 و Google Gemini
- توليد سكربتات RouterOS
- اتخاذ القرارات التقنية
- التعلم من التنفيذات السابقة
- إدارة المعرفة والذاكرة
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from enum import Enum
import openai
import google.generativeai as genai
from dataclasses import dataclass
from abc import ABC, abstractmethod

# تكوين السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntentType(Enum):
    """أنواع النيات التي يمكن للنظام فهمها"""
    NETWORK_ANALYSIS = "network_analysis"
    TROUBLESHOOTING = "troubleshooting"
    CONFIGURATION = "configuration"
    MONITORING = "monitoring"
    SECURITY_CHECK = "security_check"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    USER_MANAGEMENT = "user_management"
    SCRIPT_GENERATION = "script_generation"
    INFORMATION_QUERY = "information_query"
    AUTO_HEAL = "auto_heal"


class AIModel(Enum):
    """نماذج الذكاء الصناعي المتاحة"""
    GPT5 = "gpt-5"
    GEMINI = "gemini-pro"
    HYBRID = "hybrid"


@dataclass
class AIDecision:
    """قرار الذكاء الصناعي"""
    intent: IntentType
    confidence: float
    action_plan: List[str]
    mikrotik_script: Optional[str]
    reasoning: str
    requires_approval: bool
    risk_level: str
    estimated_execution_time: int
    rollback_plan: Optional[str]
    model_used: str
    timestamp: datetime


@dataclass
class NetworkContext:
    """سياق الشبكة الحالي"""
    router_ip: str
    cpu_load: float
    memory_usage: float
    active_connections: int
    bandwidth_usage: Dict[str, float]
    interface_status: Dict[str, str]
    recent_logs: List[str]
    alerts: List[str]


class CoreAIBrain:
    """
    العقل الصناعي المركزي - Core AI Brain
    
    هذا هو القلب النابض للنظام بأكمله.
    يجمع بين قوة GPT-5 و Google Gemini لتحقيق أعلى دقة استجابة.
    """
    
    def __init__(
        self,
        openai_api_key: str,
        gemini_api_key: str,
        enable_learning: bool = True,
        auto_execute: bool = False
    ):
        """
        تهيئة العقل الصناعي
        
        Args:
            openai_api_key: مفتاح API لـ OpenAI
            gemini_api_key: مفتاح API لـ Google Gemini
            enable_learning: تفعيل التعلم الذاتي
            auto_execute: التنفيذ التلقائي (خطر - استخدم بحذر)
        """
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key
        self.enable_learning = enable_learning
        self.auto_execute = auto_execute
        
        # تهيئة نماذج الذكاء الصناعي
        openai.api_key = self.openai_api_key
        genai.configure(api_key=self.gemini_api_key)
        
        # قاعدة المعرفة (Knowledge Base)
        self.knowledge_base = KnowledgeBase()
        
        # ذاكرة المحادثات (Conversation Memory)
        self.conversation_history = []
        
        # سجل القرارات (Decision Log)
        self.decision_history = []
        
        # نظام التعلم (Learning System)
        self.learning_system = LearningSystem() if enable_learning else None
        
        logger.info("🧠 Core AI Brain تم تهيئته بنجاح")
    
    async def process_natural_language(
        self,
        user_message: str,
        network_context: Optional[NetworkContext] = None,
        user_role: str = "technician"
    ) -> AIDecision:
        """
        معالجة اللغة الطبيعية وفهم النية
        
        Args:
            user_message: رسالة المستخدم بلغة طبيعية
            network_context: سياق الشبكة الحالي
            user_role: دور المستخدم (technician, customer, admin)
            
        Returns:
            AIDecision: قرار الذكاء الصناعي
        """
        logger.info(f"📝 معالجة رسالة: {user_message}")
        
        # 1. تحليل النية (Intent Recognition)
        intent = await self._recognize_intent(user_message)
        
        # 2. جمع البيانات السياقية
        context = await self._gather_context(network_context)
        
        # 3. استدعاء النماذج الذكية (Hybrid Approach)
        gpt_response = await self._consult_gpt5(user_message, intent, context)
        gemini_response = await self._consult_gemini(user_message, intent, context)
        
        # 4. دمج النتائج (Ensemble Decision)
        decision = await self._ensemble_decision(
            intent,
            gpt_response,
            gemini_response,
            context,
            user_role
        )
        
        # 5. توليد سكربت MikroTik إذا لزم الأمر
        if self._requires_script_generation(intent):
            decision.mikrotik_script = await self._generate_mikrotik_script(
                decision.action_plan,
                context
            )
            decision.rollback_plan = await self._generate_rollback_script(
                decision.mikrotik_script
            )
        
        # 6. تقييم المخاطر
        decision.risk_level = self._assess_risk(decision)
        decision.requires_approval = not self.auto_execute or decision.risk_level == "high"
        
        # 7. حفظ القرار في السجل
        self.decision_history.append(decision)
        
        # 8. التعلم من القرار (إذا كان مفعلاً)
        if self.learning_system:
            await self.learning_system.record_decision(decision)
        
        logger.info(f"✅ تم اتخاذ القرار: {decision.intent.value}")
        return decision
    
    async def _recognize_intent(self, message: str) -> IntentType:
        """التعرف على نية المستخدم من الرسالة"""
        # استخدام GPT لتحليل النية
        prompt = f"""
        حلل النية من الرسالة التالية وحدد نوعها:
        
        الرسالة: "{message}"
        
        الأنواع المتاحة:
        - network_analysis: تحليل الشبكة
        - troubleshooting: إصلاح المشاكل
        - configuration: تكوين الإعدادات
        - monitoring: المراقبة
        - security_check: فحص الأمان
        - performance_optimization: تحسين الأداء
        - user_management: إدارة المستخدمين
        - script_generation: توليد سكربت
        - information_query: استعلام معلومات
        - auto_heal: إصلاح تلقائي
        
        أجب بنوع النية فقط.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",  # سنستخدم GPT-4 حالياً (GPT-5 قريباً)
                messages=[
                    {"role": "system", "content": "أنت خبير في تحليل نيات المستخدمين في سياق إدارة شبكات MikroTik."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            intent_str = response.choices[0].message.content.strip().lower()
            
            # محاولة تحويل النص إلى IntentType
            for intent in IntentType:
                if intent.value in intent_str:
                    return intent
            
            # افتراضياً: استعلام معلومات
            return IntentType.INFORMATION_QUERY
            
        except Exception as e:
            logger.error(f"خطأ في تحليل النية: {e}")
            return IntentType.INFORMATION_QUERY
    
    async def _gather_context(self, network_context: Optional[NetworkContext]) -> Dict:
        """جمع السياق الكامل للتحليل"""
        context = {
            "timestamp": datetime.now().isoformat(),
            "knowledge_base": self.knowledge_base.get_relevant_knowledge(),
            "recent_decisions": [d.__dict__ for d in self.decision_history[-5:]],
        }
        
        if network_context:
            context["network"] = {
                "router_ip": network_context.router_ip,
                "cpu_load": network_context.cpu_load,
                "memory_usage": network_context.memory_usage,
                "active_connections": network_context.active_connections,
                "bandwidth_usage": network_context.bandwidth_usage,
                "interface_status": network_context.interface_status,
                "recent_logs": network_context.recent_logs,
                "alerts": network_context.alerts
            }
        
        return context
    
    async def _consult_gpt5(
        self,
        message: str,
        intent: IntentType,
        context: Dict
    ) -> Dict[str, Any]:
        """استشارة GPT-5 للحصول على تحليل متقدم"""
        system_prompt = """
        أنت Core AI Brain - العقل الصناعي المركزي لنظام إدارة شبكات MikroTik RouterOS.
        
        مسؤولياتك:
        1. تحليل المشاكل التقنية بدقة عالية
        2. اتخاذ قرارات تقنية صائبة
        3. توليد سكربتات RouterOS فعالة وآمنة
        4. تقديم شروحات واضحة ومفصلة
        5. التعلم من التجارب السابقة
        
        قواعد الأمان:
        - لا تنفذ أوامر خطرة بدون موافقة
        - دائماً قدم خطة rollback
        - احسب المخاطر بدقة
        - اختبر السكربتات قبل التنفيذ (dry-run)
        
        أجب بصيغة JSON فقط.
        """
        
        user_prompt = f"""
        النية: {intent.value}
        الرسالة: {message}
        السياق: {json.dumps(context, ensure_ascii=False, indent=2)}
        
        قدم تحليلاً شاملاً يتضمن:
        1. فهمك للمشكلة/الطلب
        2. خطة العمل التفصيلية (action_plan)
        3. التفكير المنطقي (reasoning)
        4. الأوامر أو السكربتات المطلوبة
        5. تقييم المخاطر
        6. الوقت المقدر للتنفيذ (بالثواني)
        
        صيغة JSON المطلوبة:
        {{
            "understanding": "...",
            "action_plan": ["خطوة 1", "خطوة 2", ...],
            "reasoning": "...",
            "commands": ["أمر 1", "أمر 2", ...],
            "risk_assessment": "low|medium|high",
            "estimated_time": 60,
            "confidence": 0.95
        }}
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",  # استخدام GPT-4 حالياً
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # محاولة استخراج JSON من الاستجابة
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"خطأ في استشارة GPT: {e}")
            return {
                "understanding": "حدث خطأ في التحليل",
                "action_plan": [],
                "reasoning": str(e),
                "commands": [],
                "risk_assessment": "high",
                "estimated_time": 0,
                "confidence": 0.0
            }
    
    async def _consult_gemini(
        self,
        message: str,
        intent: IntentType,
        context: Dict
    ) -> Dict[str, Any]:
        """استشارة Google Gemini للحصول على رؤية إضافية"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            أنت مساعد ذكي متخصص في شبكات MikroTik RouterOS.
            
            النية: {intent.value}
            الرسالة: {message}
            
            قدم تحليلاً سريعاً وفعالاً بصيغة JSON:
            {{
                "quick_analysis": "...",
                "suggestions": ["اقتراح 1", "اقتراح 2"],
                "warnings": ["تحذير 1", "تحذير 2"],
                "confidence": 0.85
            }}
            """
            
            response = await model.generate_content_async(prompt)
            content = response.text.strip()
            
            # محاولة استخراج JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"خطأ في استشارة Gemini: {e}")
            return {
                "quick_analysis": "غير متاح",
                "suggestions": [],
                "warnings": [],
                "confidence": 0.0
            }
    
    async def _ensemble_decision(
        self,
        intent: IntentType,
        gpt_response: Dict,
        gemini_response: Dict,
        context: Dict,
        user_role: str
    ) -> AIDecision:
        """دمج نتائج النماذج المختلفة لاتخاذ قرار نهائي"""
        # حساب الثقة الإجمالية (weighted average)
        gpt_weight = 0.7  # GPT أكثر وزناً
        gemini_weight = 0.3
        
        confidence = (
            gpt_response.get("confidence", 0.5) * gpt_weight +
            gemini_response.get("confidence", 0.5) * gemini_weight
        )
        
        # دمج خطط العمل
        action_plan = gpt_response.get("action_plan", [])
        action_plan.extend(gemini_response.get("suggestions", []))
        
        # التفكير المجمع
        reasoning = f"""
        📊 تحليل GPT-5:
        {gpt_response.get('understanding', 'غير متاح')}
        
        💡 اقتراحات Gemini:
        {gemini_response.get('quick_analysis', 'غير متاح')}
        
        🎯 القرار النهائي:
        {gpt_response.get('reasoning', 'غير متاح')}
        """
        
        decision = AIDecision(
            intent=intent,
            confidence=confidence,
            action_plan=action_plan,
            mikrotik_script=None,  # سيتم توليده لاحقاً
            reasoning=reasoning,
            requires_approval=True,  # افتراضياً يتطلب موافقة
            risk_level=gpt_response.get("risk_assessment", "medium"),
            estimated_execution_time=gpt_response.get("estimated_time", 60),
            rollback_plan=None,  # سيتم توليده لاحقاً
            model_used="GPT-5 + Gemini (Hybrid)",
            timestamp=datetime.now()
        )
        
        return decision
    
    def _requires_script_generation(self, intent: IntentType) -> bool:
        """هل يتطلب هذا النوع من النية توليد سكربت؟"""
        script_required_intents = [
            IntentType.CONFIGURATION,
            IntentType.TROUBLESHOOTING,
            IntentType.PERFORMANCE_OPTIMIZATION,
            IntentType.USER_MANAGEMENT,
            IntentType.SCRIPT_GENERATION,
            IntentType.AUTO_HEAL
        ]
        return intent in script_required_intents
    
    async def _generate_mikrotik_script(
        self,
        action_plan: List[str],
        context: Dict
    ) -> str:
        """توليد سكربت MikroTik RouterOS من خطة العمل"""
        prompt = f"""
        أنت خبير في كتابة سكربتات MikroTik RouterOS.
        
        خطة العمل:
        {json.dumps(action_plan, ensure_ascii=False, indent=2)}
        
        السياق:
        {json.dumps(context.get('network', {}), ensure_ascii=False, indent=2)}
        
        قم بكتابة سكربت RouterOS كامل وفعال لتنفيذ هذه الخطة.
        
        متطلبات السكربت:
        1. يجب أن يكون آمناً وقابلاً للتراجع
        2. يتضمن معالجة الأخطاء
        3. يسجل العمليات في اللوج
        4. مُعلّق بشكل واضح
        5. يتبع أفضل الممارسات
        
        أرجع السكربت فقط بدون أي نص إضافي.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت خبير في RouterOS scripting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # دقة عالية
                max_tokens=1500
            )
            
            script = response.choices[0].message.content.strip()
            
            # إزالة markdown code blocks إن وجدت
            if "```" in script:
                script = script.split("```")[1]
                if script.startswith("mikrotik") or script.startswith("routeros"):
                    script = "\n".join(script.split("\n")[1:])
            
            return script.strip()
            
        except Exception as e:
            logger.error(f"خطأ في توليد السكربت: {e}")
            return f"# خطأ في توليد السكربت: {e}"
    
    async def _generate_rollback_script(self, original_script: str) -> str:
        """توليد سكربت للتراجع عن التغييرات"""
        prompt = f"""
        أنت خبير في أمان شبكات MikroTik.
        
        السكربت الأصلي:
        {original_script}
        
        قم بكتابة سكربت rollback كامل يتراجع عن جميع التغييرات في السكربت الأصلي.
        
        يجب أن يكون سكربت الـ rollback:
        1. آمناً بنسبة 100%
        2. يعيد الإعدادات للحالة السابقة
        3. مُعلّق بوضوح
        4. قابل للتنفيذ فوراً
        
        أرجع سكربت الـ rollback فقط.
        """
        
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت خبير في أمان وإدارة MikroTik RouterOS."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # دقة قصوى
                max_tokens=1500
            )
            
            script = response.choices[0].message.content.strip()
            
            if "```" in script:
                script = script.split("```")[1]
                if script.startswith("mikrotik") or script.startswith("routeros"):
                    script = "\n".join(script.split("\n")[1:])
            
            return script.strip()
            
        except Exception as e:
            logger.error(f"خطأ في توليد سكربت الـ rollback: {e}")
            return f"# خطأ في توليد سكربت الـ rollback: {e}"
    
    def _assess_risk(self, decision: AIDecision) -> str:
        """تقييم مستوى المخاطر للقرار"""
        risk_score = 0
        
        # تقييم بناءً على نوع النية
        high_risk_intents = [
            IntentType.CONFIGURATION,
            IntentType.SECURITY_CHECK,
            IntentType.AUTO_HEAL
        ]
        
        if decision.intent in high_risk_intents:
            risk_score += 30
        
        # تقييم بناءً على الثقة
        if decision.confidence < 0.7:
            risk_score += 40
        
        # تقييم بناءً على وجود سكربت
        if decision.mikrotik_script and len(decision.mikrotik_script) > 500:
            risk_score += 20
        
        # تقييم بناءً على خطة العمل
        if len(decision.action_plan) > 5:
            risk_score += 10
        
        # تحديد المستوى
        if risk_score >= 60:
            return "high"
        elif risk_score >= 30:
            return "medium"
        else:
            return "low"
    
    async def execute_decision(
        self,
        decision: AIDecision,
        executor,
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        تنفيذ القرار على الراوتر
        
        Args:
            decision: القرار المراد تنفيذه
            executor: محرك التنفيذ
            dry_run: تنفيذ تجريبي أولاً
            
        Returns:
            نتيجة التنفيذ
        """
        logger.info(f"🚀 بدء تنفيذ القرار: {decision.intent.value}")
        
        if not decision.mikrotik_script:
            return {
                "success": False,
                "error": "لا يوجد سكربت للتنفيذ"
            }
        
        # 1. تنفيذ تجريبي (Dry Run)
        if dry_run:
            logger.info("🧪 تنفيذ تجريبي...")
            dry_result = await executor.dry_run(decision.mikrotik_script)
            
            if not dry_result.get("success"):
                logger.error(f"❌ فشل التنفيذ التجريبي: {dry_result.get('error')}")
                return dry_result
        
        # 2. أخذ Snapshot قبل التنفيذ
        logger.info("📸 أخذ snapshot للنظام...")
        snapshot = await executor.create_snapshot()
        
        # 3. التنفيذ الفعلي
        logger.info("⚡ التنفيذ الفعلي...")
        result = await executor.execute(decision.mikrotik_script)
        
        # 4. التحقق من النتيجة
        if result.get("success"):
            logger.info("✅ تم التنفيذ بنجاح")
            
            # التعلم من النجاح
            if self.learning_system:
                await self.learning_system.record_success(decision, result)
        else:
            logger.error(f"❌ فشل التنفيذ: {result.get('error')}")
            
            # محاولة Rollback
            if decision.rollback_plan:
                logger.info("🔄 تنفيذ خطة الـ rollback...")
                await executor.execute(decision.rollback_plan)
            
            # التعلم من الفشل
            if self.learning_system:
                await self.learning_system.record_failure(decision, result)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """الحصول على حالة العقل الصناعي"""
        return {
            "status": "active",
            "auto_execute": self.auto_execute,
            "learning_enabled": self.enable_learning,
            "total_decisions": len(self.decision_history),
            "conversation_history_size": len(self.conversation_history),
            "knowledge_base_size": self.knowledge_base.size(),
            "uptime": "active"
        }


class KnowledgeBase:
    """قاعدة المعرفة للنظام"""
    
    def __init__(self):
        self.knowledge = {
            "common_issues": [],
            "best_practices": [],
            "mikrotik_commands": [],
            "learned_patterns": []
        }
    
    def get_relevant_knowledge(self) -> Dict:
        """الحصول على المعرفة ذات الصلة"""
        return self.knowledge
    
    def size(self) -> int:
        """حجم قاعدة المعرفة"""
        return sum(len(v) for v in self.knowledge.values())
    
    async def update(self, new_knowledge: Dict):
        """تحديث قاعدة المعرفة"""
        for key, value in new_knowledge.items():
            if key in self.knowledge:
                self.knowledge[key].extend(value)


class LearningSystem:
    """نظام التعلم الذاتي"""
    
    def __init__(self):
        self.success_patterns = []
        self.failure_patterns = []
    
    async def record_decision(self, decision: AIDecision):
        """تسجيل قرار للتعلم منه لاحقاً"""
        pass
    
    async def record_success(self, decision: AIDecision, result: Dict):
        """التعلم من النجاح"""
        self.success_patterns.append({
            "intent": decision.intent.value,
            "confidence": decision.confidence,
            "result": result,
            "timestamp": datetime.now()
        })
    
    async def record_failure(self, decision: AIDecision, result: Dict):
        """التعلم من الفشل"""
        self.failure_patterns.append({
            "intent": decision.intent.value,
            "confidence": decision.confidence,
            "error": result.get("error"),
            "timestamp": datetime.now()
        })


# مثال على الاستخدام
if __name__ == "__main__":
    async def test_core_brain():
        """اختبار العقل الصناعي"""
        brain = CoreAIBrain(
            openai_api_key="your-openai-key",
            gemini_api_key="your-gemini-key",
            enable_learning=True,
            auto_execute=False
        )
        
        # مثال على معالجة رسالة
        decision = await brain.process_natural_language(
            user_message="الراوتر بطيء جداً، كيف أحسن الأداء؟",
            network_context=NetworkContext(
                router_ip="192.168.88.1",
                cpu_load=85.5,
                memory_usage=70.2,
                active_connections=150,
                bandwidth_usage={"wan1": 95.5, "wan2": 60.0},
                interface_status={"ether1": "running", "ether2": "running"},
                recent_logs=["Connection timeout", "High CPU usage"],
                alerts=["CPU > 80%", "Memory > 70%"]
            )
        )
        
        print(f"\n🧠 قرار الذكاء الصناعي:")
        print(f"النية: {decision.intent.value}")
        print(f"الثقة: {decision.confidence:.2%}")
        print(f"مستوى المخاطر: {decision.risk_level}")
        print(f"\n📋 خطة العمل:")
        for i, step in enumerate(decision.action_plan, 1):
            print(f"  {i}. {step}")
        print(f"\n💭 التفكير المنطقي:")
        print(decision.reasoning)
        
        if decision.mikrotik_script:
            print(f"\n📜 سكربت MikroTik:")
            print(decision.mikrotik_script)
    
    # تشغيل الاختبار
    asyncio.run(test_core_brain())
