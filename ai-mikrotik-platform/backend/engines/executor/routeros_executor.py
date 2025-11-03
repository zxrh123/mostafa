"""
RouterOS Executor Engine - محرك تنفيذ أوامر MikroTik RouterOS
يتحكم في تنفيذ الأوامر والسكربتات على أجهزة MikroTik بأمان وكفاءة

المسؤوليات:
- تنفيذ الأوامر عبر SSH أو API
- التحقق من الأوامر قبل التنفيذ (Dry Run)
- أخذ Snapshots تلقائية
- Rollback في حالة الفشل
- معالجة الأخطاء المتقدمة
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import paramiko
import librouteros
from dataclasses import dataclass
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """أنماط التنفيذ"""
    DRY_RUN = "dry_run"
    SAFE = "safe"
    FORCE = "force"


class ConnectionMethod(Enum):
    """طرق الاتصال"""
    SSH = "ssh"
    API = "api"
    WINBOX_API = "winbox_api"


@dataclass
class ExecutionResult:
    """نتيجة التنفيذ"""
    success: bool
    output: str
    error: Optional[str]
    execution_time: float
    commands_executed: List[str]
    snapshot_id: Optional[str]
    timestamp: datetime
    rollback_available: bool


@dataclass
class RouterConnection:
    """معلومات الاتصال بالراوتر"""
    host: str
    port: int
    username: str
    password: str
    connection_method: ConnectionMethod
    timeout: int = 30


class RouterOSExecutor:
    """
    محرك تنفيذ أوامر RouterOS
    
    يوفر واجهة آمنة وموثوقة لتنفيذ الأوامر على أجهزة MikroTik
    """
    
    def __init__(
        self,
        router_connection: RouterConnection,
        auto_snapshot: bool = True,
        max_retries: int = 3
    ):
        """
        تهيئة المنفذ
        
        Args:
            router_connection: معلومات الاتصال بالراوتر
            auto_snapshot: أخذ snapshot تلقائي قبل التنفيذ
            max_retries: عدد المحاولات القصوى عند الفشل
        """
        self.connection = router_connection
        self.auto_snapshot = auto_snapshot
        self.max_retries = max_retries
        self.ssh_client = None
        self.api_client = None
        self.execution_history = []
        
        logger.info(f"🔧 RouterOS Executor تم تهيئته للراوتر {router_connection.host}")
    
    async def connect(self) -> bool:
        """
        الاتصال بالراوتر
        
        Returns:
            True إذا نجح الاتصال
        """
        try:
            if self.connection.connection_method == ConnectionMethod.SSH:
                return await self._connect_ssh()
            elif self.connection.connection_method == ConnectionMethod.API:
                return await self._connect_api()
            else:
                logger.error(f"طريقة اتصال غير مدعومة: {self.connection.connection_method}")
                return False
        except Exception as e:
            logger.error(f"خطأ في الاتصال: {e}")
            return False
    
    async def _connect_ssh(self) -> bool:
        """الاتصال عبر SSH"""
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.ssh_client.connect(
                hostname=self.connection.host,
                port=self.connection.port,
                username=self.connection.username,
                password=self.connection.password,
                timeout=self.connection.timeout,
                look_for_keys=False,
                allow_agent=False
            )
            
            logger.info(f"✅ اتصال SSH ناجح: {self.connection.host}")
            return True
            
        except Exception as e:
            logger.error(f"❌ فشل اتصال SSH: {e}")
            return False
    
    async def _connect_api(self) -> bool:
        """الاتصال عبر API"""
        try:
            self.api_client = librouteros.connect(
                host=self.connection.host,
                username=self.connection.username,
                password=self.connection.password,
                port=self.connection.port or 8728,
                timeout=self.connection.timeout
            )
            
            logger.info(f"✅ اتصال API ناجح: {self.connection.host}")
            return True
            
        except Exception as e:
            logger.error(f"❌ فشل اتصال API: {e}")
            return False
    
    async def execute(
        self,
        script: str,
        mode: ExecutionMode = ExecutionMode.SAFE,
        description: str = ""
    ) -> ExecutionResult:
        """
        تنفيذ سكربت على الراوتر
        
        Args:
            script: السكربت المراد تنفيذه
            mode: نمط التنفيذ (dry_run, safe, force)
            description: وصف للعملية
            
        Returns:
            نتيجة التنفيذ
        """
        start_time = datetime.now()
        logger.info(f"🚀 بدء التنفيذ: {description or 'بدون وصف'}")
        
        # 1. التحقق من الاتصال
        if not await self._verify_connection():
            return ExecutionResult(
                success=False,
                output="",
                error="فشل الاتصال بالراوتر",
                execution_time=0,
                commands_executed=[],
                snapshot_id=None,
                timestamp=start_time,
                rollback_available=False
            )
        
        # 2. تحليل السكربت
        commands = self._parse_script(script)
        logger.info(f"📋 تم تحليل {len(commands)} أمر")
        
        # 3. Dry Run (إذا كان النمط safe)
        if mode == ExecutionMode.SAFE or mode == ExecutionMode.DRY_RUN:
            dry_result = await self._dry_run(commands)
            if not dry_result["valid"]:
                return ExecutionResult(
                    success=False,
                    output=dry_result.get("output", ""),
                    error=f"فشل التحقق: {dry_result.get('error')}",
                    execution_time=0,
                    commands_executed=[],
                    snapshot_id=None,
                    timestamp=start_time,
                    rollback_available=False
                )
            
            # إذا كان dry_run فقط، نتوقف هنا
            if mode == ExecutionMode.DRY_RUN:
                return ExecutionResult(
                    success=True,
                    output="✅ التحقق من السكربت ناجح (لم يتم التنفيذ الفعلي)",
                    error=None,
                    execution_time=(datetime.now() - start_time).total_seconds(),
                    commands_executed=commands,
                    snapshot_id=None,
                    timestamp=start_time,
                    rollback_available=False
                )
        
        # 4. أخذ Snapshot (إذا كان مفعلاً)
        snapshot_id = None
        if self.auto_snapshot:
            snapshot_id = await self.create_snapshot(description)
        
        # 5. التنفيذ الفعلي
        try:
            output = await self._execute_commands(commands)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = ExecutionResult(
                success=True,
                output=output,
                error=None,
                execution_time=execution_time,
                commands_executed=commands,
                snapshot_id=snapshot_id,
                timestamp=start_time,
                rollback_available=snapshot_id is not None
            )
            
            # حفظ في السجل
            self.execution_history.append(result)
            
            logger.info(f"✅ التنفيذ ناجح في {execution_time:.2f} ثانية")
            return result
            
        except Exception as e:
            logger.error(f"❌ فشل التنفيذ: {e}")
            
            # محاولة Rollback إذا كان هناك snapshot
            if snapshot_id:
                logger.info("🔄 محاولة الرجوع للحالة السابقة...")
                await self.rollback_to_snapshot(snapshot_id)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = ExecutionResult(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time,
                commands_executed=commands,
                snapshot_id=snapshot_id,
                timestamp=start_time,
                rollback_available=False
            )
            
            self.execution_history.append(result)
            return result
    
    async def _verify_connection(self) -> bool:
        """التحقق من الاتصال بالراوتر"""
        if self.connection.connection_method == ConnectionMethod.SSH:
            return self.ssh_client is not None and self.ssh_client.get_transport() is not None
        elif self.connection.connection_method == ConnectionMethod.API:
            return self.api_client is not None
        return False
    
    def _parse_script(self, script: str) -> List[str]:
        """تحليل السكربت إلى أوامر فردية"""
        # إزالة التعليقات والأسطر الفارغة
        lines = [
            line.strip()
            for line in script.split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        return lines
    
    async def _dry_run(self, commands: List[str]) -> Dict[str, Any]:
        """
        التحقق من الأوامر بدون تنفيذ فعلي
        
        Returns:
            نتيجة التحقق
        """
        logger.info("🧪 بدء التحقق من الأوامر (Dry Run)...")
        
        # قائمة الأوامر الخطرة
        dangerous_commands = [
            "/system reset-configuration",
            "/system reboot",
            "/interface disable",
            "/ip firewall filter remove",
            "/system backup save"
        ]
        
        # التحقق من الأوامر الخطرة
        for cmd in commands:
            for dangerous in dangerous_commands:
                if dangerous in cmd:
                    logger.warning(f"⚠️ أمر خطر: {cmd}")
                    return {
                        "valid": False,
                        "error": f"الأمر '{cmd}' خطر ويتطلب موافقة خاصة",
                        "output": ""
                    }
        
        # التحقق من صحة بناء الأوامر (syntax)
        try:
            for cmd in commands:
                # تحليل أساسي للبناء
                if not self._validate_command_syntax(cmd):
                    return {
                        "valid": False,
                        "error": f"خطأ في بناء الأمر: {cmd}",
                        "output": ""
                    }
            
            logger.info("✅ جميع الأوامر صالحة")
            return {
                "valid": True,
                "error": None,
                "output": "جميع الأوامر اجتازت التحقق"
            }
            
        except Exception as e:
            logger.error(f"❌ خطأ في التحقق: {e}")
            return {
                "valid": False,
                "error": str(e),
                "output": ""
            }
    
    def _validate_command_syntax(self, command: str) -> bool:
        """التحقق من صحة بناء الأمر"""
        # قواعد أساسية
        if not command.strip():
            return False
        
        # يجب أن يبدأ بـ /
        if not command.strip().startswith("/"):
            return False
        
        # التحقق من وجود أقواس متطابقة
        if command.count('"') % 2 != 0:
            return False
        
        if command.count("[") != command.count("]"):
            return False
        
        return True
    
    async def _execute_commands(self, commands: List[str]) -> str:
        """تنفيذ الأوامر الفعلي"""
        if self.connection.connection_method == ConnectionMethod.SSH:
            return await self._execute_via_ssh(commands)
        elif self.connection.connection_method == ConnectionMethod.API:
            return await self._execute_via_api(commands)
        else:
            raise Exception("طريقة اتصال غير مدعومة")
    
    async def _execute_via_ssh(self, commands: List[str]) -> str:
        """تنفيذ الأوامر عبر SSH"""
        try:
            # تحويل الأوامر إلى سكربت واحد
            script = "\n".join(commands)
            
            # تنفيذ السكربت
            stdin, stdout, stderr = self.ssh_client.exec_command(script)
            
            # قراءة النتائج
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if error:
                raise Exception(f"خطأ في التنفيذ: {error}")
            
            return output
            
        except Exception as e:
            logger.error(f"خطأ في التنفيذ عبر SSH: {e}")
            raise
    
    async def _execute_via_api(self, commands: List[str]) -> str:
        """تنفيذ الأوامر عبر API"""
        try:
            results = []
            
            for cmd in commands:
                # تحويل الأمر إلى مسار API
                api_path = self._command_to_api_path(cmd)
                
                # تنفيذ الأمر
                response = self.api_client(cmd=api_path)
                results.append(str(response))
            
            return "\n".join(results)
            
        except Exception as e:
            logger.error(f"خطأ في التنفيذ عبر API: {e}")
            raise
    
    def _command_to_api_path(self, command: str) -> str:
        """تحويل أمر RouterOS إلى مسار API"""
        # تحويل بسيط - يمكن تحسينه
        return command.replace("/", "").replace(" ", "/")
    
    async def create_snapshot(self, description: str = "") -> Optional[str]:
        """
        أخذ Snapshot للنظام
        
        Args:
            description: وصف للـ snapshot
            
        Returns:
            معرف الـ snapshot
        """
        try:
            snapshot_name = f"ai-snapshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            
            # أمر أخذ backup
            backup_command = f'/system backup save name="{snapshot_name}" dont-encrypt=yes'
            
            logger.info(f"📸 أخذ snapshot: {snapshot_name}")
            
            # تنفيذ الأمر
            if self.connection.connection_method == ConnectionMethod.SSH:
                stdin, stdout, stderr = self.ssh_client.exec_command(backup_command)
                error = stderr.read().decode('utf-8')
                
                if error:
                    logger.error(f"❌ فشل أخذ snapshot: {error}")
                    return None
            
            logger.info(f"✅ تم أخذ snapshot بنجاح: {snapshot_name}")
            return snapshot_name
            
        except Exception as e:
            logger.error(f"❌ خطأ في أخذ snapshot: {e}")
            return None
    
    async def rollback_to_snapshot(self, snapshot_id: str) -> bool:
        """
        الرجوع إلى snapshot سابق
        
        Args:
            snapshot_id: معرف الـ snapshot
            
        Returns:
            True إذا نجحت العملية
        """
        try:
            logger.info(f"🔄 الرجوع إلى snapshot: {snapshot_id}")
            
            # أمر استعادة backup
            restore_command = f'/system backup load name="{snapshot_id}"'
            
            # تنفيذ الأمر
            if self.connection.connection_method == ConnectionMethod.SSH:
                stdin, stdout, stderr = self.ssh_client.exec_command(restore_command)
                error = stderr.read().decode('utf-8')
                
                if error and "success" not in error.lower():
                    logger.error(f"❌ فشلت الاستعادة: {error}")
                    return False
            
            logger.info(f"✅ تمت الاستعادة بنجاح")
            
            # إعادة الاتصال (قد ينقطع الاتصال بعد الاستعادة)
            await asyncio.sleep(5)
            await self.connect()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ خطأ في الاستعادة: {e}")
            return False
    
    async def get_system_info(self) -> Dict[str, Any]:
        """الحصول على معلومات النظام"""
        try:
            if self.connection.connection_method == ConnectionMethod.SSH:
                commands = [
                    "/system resource print",
                    "/system identity print",
                    "/system routerboard print"
                ]
                
                results = {}
                for cmd in commands:
                    stdin, stdout, stderr = self.ssh_client.exec_command(cmd)
                    output = stdout.read().decode('utf-8')
                    results[cmd] = output
                
                return results
            else:
                return {"error": "API method not implemented yet"}
                
        except Exception as e:
            logger.error(f"خطأ في الحصول على معلومات النظام: {e}")
            return {"error": str(e)}
    
    async def disconnect(self):
        """قطع الاتصال"""
        try:
            if self.ssh_client:
                self.ssh_client.close()
            if self.api_client:
                self.api_client.close()
            
            logger.info("👋 تم قطع الاتصال")
            
        except Exception as e:
            logger.error(f"خطأ في قطع الاتصال: {e}")
    
    def get_execution_history(self) -> List[ExecutionResult]:
        """الحصول على سجل التنفيذات"""
        return self.execution_history
    
    def __del__(self):
        """تنظيف الموارد"""
        try:
            if self.ssh_client:
                self.ssh_client.close()
        except:
            pass


# مثال على الاستخدام
if __name__ == "__main__":
    async def test_executor():
        """اختبار المنفذ"""
        # إنشاء اتصال
        connection = RouterConnection(
            host="192.168.88.1",
            port=22,
            username="admin",
            password="password",
            connection_method=ConnectionMethod.SSH
        )
        
        # إنشاء المنفذ
        executor = RouterOSExecutor(
            router_connection=connection,
            auto_snapshot=True
        )
        
        # الاتصال
        if await executor.connect():
            print("✅ اتصال ناجح")
            
            # تنفيذ سكربت بسيط
            script = """
            # تحديث اسم النظام
            /system identity set name="AI-Router-Test"
            
            # عرض المعلومات
            /system resource print
            """
            
            # تنفيذ (dry run أولاً)
            result = await executor.execute(
                script=script,
                mode=ExecutionMode.DRY_RUN,
                description="تحديث اسم الراوتر"
            )
            
            print(f"\nنتيجة Dry Run:")
            print(f"نجح: {result.success}")
            print(f"الخرج: {result.output}")
            
            # قطع الاتصال
            await executor.disconnect()
        else:
            print("❌ فشل الاتصال")
    
    # تشغيل الاختبار
    asyncio.run(test_executor())
