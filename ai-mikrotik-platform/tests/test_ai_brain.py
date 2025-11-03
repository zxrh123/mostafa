"""
اختبارات العقل الصناعي - Core AI Brain Tests
"""

import pytest
import asyncio
from datetime import datetime
import sys
sys.path.append('../backend')
sys.path.append('../ai-core')

from ai_core.brain.core_ai_brain import (
    CoreAIBrain,
    IntentType,
    NetworkContext,
    AIDecision
)


@pytest.fixture
def ai_brain():
    """إنشاء instance من العقل الصناعي للاختبار"""
    return CoreAIBrain(
        openai_api_key="test-key",
        gemini_api_key="test-key",
        enable_learning=True,
        auto_execute=False
    )


@pytest.fixture
def network_context():
    """سياق شبكة للاختبار"""
    return NetworkContext(
        router_ip="192.168.88.1",
        cpu_load=75.5,
        memory_usage=65.0,
        active_connections=150,
        bandwidth_usage={"wan1": 80.0, "wan2": 60.0},
        interface_status={"ether1": "running", "ether2": "running"},
        recent_logs=["Connection established", "High CPU usage"],
        alerts=["CPU > 70%", "Memory > 60%"]
    )


class TestCoreAIBrain:
    """اختبارات العقل الصناعي المركزي"""
    
    def test_initialization(self, ai_brain):
        """اختبار التهيئة الأساسية"""
        assert ai_brain is not None
        assert ai_brain.enable_learning == True
        assert ai_brain.auto_execute == False
        assert ai_brain.knowledge_base is not None
        assert len(ai_brain.decision_history) == 0
    
    @pytest.mark.asyncio
    async def test_intent_recognition(self, ai_brain):
        """اختبار التعرف على النية"""
        # اختبار رسالة استعلام
        intent = await ai_brain._recognize_intent("ما حالة الراوتر؟")
        assert isinstance(intent, IntentType)
        
        # اختبار رسالة إصلاح
        intent = await ai_brain._recognize_intent("الراوتر بطيء، كيف أحسن الأداء؟")
        assert intent in [IntentType.TROUBLESHOOTING, IntentType.PERFORMANCE_OPTIMIZATION]
    
    @pytest.mark.asyncio
    async def test_context_gathering(self, ai_brain, network_context):
        """اختبار جمع السياق"""
        context = await ai_brain._gather_context(network_context)
        
        assert "timestamp" in context
        assert "knowledge_base" in context
        assert "network" in context
        assert context["network"]["router_ip"] == "192.168.88.1"
        assert context["network"]["cpu_load"] == 75.5
    
    @pytest.mark.asyncio
    async def test_process_natural_language(self, ai_brain, network_context):
        """اختبار معالجة اللغة الطبيعية"""
        decision = await ai_brain.process_natural_language(
            user_message="عرض معلومات النظام",
            network_context=network_context,
            user_role="technician"
        )
        
        assert isinstance(decision, AIDecision)
        assert decision.intent is not None
        assert 0 <= decision.confidence <= 1
        assert isinstance(decision.action_plan, list)
        assert decision.risk_level in ["low", "medium", "high"]
    
    def test_requires_script_generation(self, ai_brain):
        """اختبار تحديد متى يتطلب توليد سكربت"""
        # يتطلب سكربت
        assert ai_brain._requires_script_generation(IntentType.CONFIGURATION) == True
        assert ai_brain._requires_script_generation(IntentType.TROUBLESHOOTING) == True
        
        # لا يتطلب سكربت
        assert ai_brain._requires_script_generation(IntentType.INFORMATION_QUERY) == False
    
    def test_risk_assessment(self, ai_brain):
        """اختبار تقييم المخاطر"""
        decision = AIDecision(
            intent=IntentType.CONFIGURATION,
            confidence=0.5,
            action_plan=["step1", "step2"],
            mikrotik_script="/system identity set name=\"test\"",
            reasoning="test",
            requires_approval=True,
            risk_level="",
            estimated_execution_time=60,
            rollback_plan=None,
            model_used="test",
            timestamp=datetime.now()
        )
        
        risk = ai_brain._assess_risk(decision)
        assert risk in ["low", "medium", "high"]
    
    def test_get_status(self, ai_brain):
        """اختبار الحصول على الحالة"""
        status = ai_brain.get_status()
        
        assert "status" in status
        assert "auto_execute" in status
        assert "learning_enabled" in status
        assert "total_decisions" in status


class TestKnowledgeBase:
    """اختبارات قاعدة المعرفة"""
    
    def test_knowledge_base_initialization(self, ai_brain):
        """اختبار تهيئة قاعدة المعرفة"""
        kb = ai_brain.knowledge_base
        assert kb is not None
        assert isinstance(kb.knowledge, dict)
    
    def test_knowledge_base_size(self, ai_brain):
        """اختبار حجم قاعدة المعرفة"""
        kb = ai_brain.knowledge_base
        size = kb.size()
        assert isinstance(size, int)
        assert size >= 0


class TestLearningSystem:
    """اختبارات نظام التعلم"""
    
    def test_learning_system_initialization(self, ai_brain):
        """اختبار تهيئة نظام التعلم"""
        ls = ai_brain.learning_system
        assert ls is not None
        assert isinstance(ls.success_patterns, list)
        assert isinstance(ls.failure_patterns, list)
    
    @pytest.mark.asyncio
    async def test_record_success(self, ai_brain):
        """اختبار تسجيل النجاح"""
        decision = AIDecision(
            intent=IntentType.CONFIGURATION,
            confidence=0.9,
            action_plan=["test"],
            mikrotik_script="test",
            reasoning="test",
            requires_approval=False,
            risk_level="low",
            estimated_execution_time=60,
            rollback_plan=None,
            model_used="test",
            timestamp=datetime.now()
        )
        
        await ai_brain.learning_system.record_success(decision, {"success": True})
        
        assert len(ai_brain.learning_system.success_patterns) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
