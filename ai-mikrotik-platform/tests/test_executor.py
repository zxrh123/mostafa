"""
اختبارات محرك التنفيذ - Executor Engine Tests
"""

import pytest
import asyncio
import sys
sys.path.append('../backend')

from backend.engines.executor.routeros_executor import (
    RouterOSExecutor,
    RouterConnection,
    ConnectionMethod,
    ExecutionMode,
    ExecutionResult
)


@pytest.fixture
def router_connection():
    """إنشاء اتصال للاختبار"""
    return RouterConnection(
        host="192.168.88.1",
        port=22,
        username="admin",
        password="test",
        connection_method=ConnectionMethod.SSH,
        timeout=30
    )


@pytest.fixture
def executor(router_connection):
    """إنشاء executor للاختبار"""
    return RouterOSExecutor(
        router_connection=router_connection,
        auto_snapshot=True,
        max_retries=3
    )


class TestRouterOSExecutor:
    """اختبارات محرك تنفيذ RouterOS"""
    
    def test_initialization(self, executor):
        """اختبار التهيئة الأساسية"""
        assert executor is not None
        assert executor.auto_snapshot == True
        assert executor.max_retries == 3
        assert len(executor.execution_history) == 0
    
    def test_parse_script(self, executor):
        """اختبار تحليل السكربت"""
        script = """
        # تعليق
        /system identity set name="test"
        /system resource print
        
        # تعليق آخر
        /interface print
        """
        
        commands = executor._parse_script(script)
        
        assert len(commands) == 3
        assert "/system identity" in commands[0]
        assert "/system resource" in commands[1]
        assert "/interface print" in commands[2]
    
    def test_validate_command_syntax(self, executor):
        """اختبار التحقق من صحة بناء الأمر"""
        # أوامر صحيحة
        assert executor._validate_command_syntax('/system identity print') == True
        assert executor._validate_command_syntax('/interface print') == True
        
        # أوامر خاطئة
        assert executor._validate_command_syntax('system identity print') == False  # بدون /
        assert executor._validate_command_syntax('') == False  # فارغ
        assert executor._validate_command_syntax('/system "test') == False  # أقواس غير متطابقة
    
    @pytest.mark.asyncio
    async def test_dry_run(self, executor):
        """اختبار التنفيذ التجريبي"""
        commands = [
            "/system identity print",
            "/system resource print"
        ]
        
        result = await executor._dry_run(commands)
        
        assert isinstance(result, dict)
        assert "valid" in result
        assert "error" in result or result["valid"] == True
    
    @pytest.mark.asyncio
    async def test_dangerous_commands_detection(self, executor):
        """اختبار كشف الأوامر الخطرة"""
        dangerous = [
            "/system reset-configuration",
            "/system reboot"
        ]
        
        result = await executor._dry_run(dangerous)
        
        assert result["valid"] == False
        assert "error" in result
    
    def test_get_execution_history(self, executor):
        """اختبار الحصول على سجل التنفيذات"""
        history = executor.get_execution_history()
        
        assert isinstance(history, list)


class TestExecutionResult:
    """اختبارات نتيجة التنفيذ"""
    
    def test_execution_result_structure(self):
        """اختبار بنية نتيجة التنفيذ"""
        from datetime import datetime
        
        result = ExecutionResult(
            success=True,
            output="test output",
            error=None,
            execution_time=1.5,
            commands_executed=["test"],
            snapshot_id="snap-123",
            timestamp=datetime.now(),
            rollback_available=True
        )
        
        assert result.success == True
        assert result.output == "test output"
        assert result.execution_time == 1.5
        assert result.rollback_available == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
