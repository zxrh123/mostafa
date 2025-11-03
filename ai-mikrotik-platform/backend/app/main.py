"""
FastAPI Main Application - التطبيق الرئيسي للـ Backend
نقطة الدخول الرئيسية لنظام إدارة MikroTik الذكي

المسؤوليات:
- إنشاء تطبيق FastAPI
- تكوين CORS والأمان
- تسجيل المسارات (Routes)
- إدارة WebSocket
- ربط جميع المكونات معاً
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import json

# استيراد المحركات
import sys
sys.path.append('..')
from engines.executor.routeros_executor import RouterOSExecutor, RouterConnection, ConnectionMethod
from engines.monitoring.network_monitor import NetworkMonitor, Alert
from ai_core.brain.core_ai_brain import CoreAIBrain, NetworkContext, IntentType

# تكوين السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# إدارة الاتصالات النشطة WebSocket
class ConnectionManager:
    """إدارة اتصالات WebSocket"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """قبول اتصال جديد"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"✅ اتصال WebSocket جديد. الإجمالي: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """قطع اتصال"""
        self.active_connections.remove(websocket)
        logger.info(f"👋 قطع اتصال WebSocket. المتبقي: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """إرسال رسالة لاتصال محدد"""
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        """بث رسالة لجميع الاتصالات"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


# متغيرات عامة
ai_brain: Optional[CoreAIBrain] = None
executor: Optional[RouterOSExecutor] = None
monitor: Optional[NetworkMonitor] = None
connection_manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """إدارة دورة حياة التطبيق"""
    logger.info("🚀 بدء تشغيل النظام...")
    
    # تهيئة المكونات
    await initialize_system()
    
    # بدء المراقبة
    if monitor:
        await monitor.start_monitoring()
    
    logger.info("✅ النظام جاهز!")
    
    yield
    
    # تنظيف عند الإيقاف
    logger.info("🛑 إيقاف النظام...")
    
    if monitor:
        await monitor.stop_monitoring()
    
    if executor:
        await executor.disconnect()
    
    logger.info("👋 تم إيقاف النظام بنجاح")


# إنشاء تطبيق FastAPI
app = FastAPI(
    title="🧠 AI-Powered MikroTik Management Platform",
    description="منصة ذكاء صناعي متكاملة لإدارة شبكات MikroTik RouterOS",
    version="1.0.0",
    lifespan=lifespan
)


# تكوين CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # في الإنتاج: حدد النطاقات المسموحة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def initialize_system():
    """تهيئة جميع مكونات النظام"""
    global ai_brain, executor, monitor
    
    try:
        # 1. تهيئة العقل الصناعي
        logger.info("🧠 تهيئة Core AI Brain...")
        ai_brain = CoreAIBrain(
            openai_api_key="your-openai-api-key-here",  # من متغيرات البيئة
            gemini_api_key="your-gemini-api-key-here",
            enable_learning=True,
            auto_execute=False
        )
        
        # 2. تهيئة محرك التنفيذ
        logger.info("🔧 تهيئة RouterOS Executor...")
        router_config = RouterConnection(
            host="192.168.88.1",  # من التكوين
            port=22,
            username="admin",
            password="password",
            connection_method=ConnectionMethod.SSH,
            timeout=30
        )
        
        executor = RouterOSExecutor(
            router_connection=router_config,
            auto_snapshot=True,
            max_retries=3
        )
        
        # الاتصال بالراوتر
        connected = await executor.connect()
        if not connected:
            logger.error("❌ فشل الاتصال بالراوتر")
        
        # 3. تهيئة محرك المراقبة
        logger.info("📊 تهيئة Network Monitor...")
        monitor = NetworkMonitor(
            executor=executor,
            check_interval=30,
            enable_auto_heal=True
        )
        
        # إضافة callback للتنبيهات
        monitor.add_alert_callback(handle_alert)
        
        logger.info("✅ تم تهيئة جميع المكونات")
        
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة النظام: {e}")


async def handle_alert(alert: Alert):
    """معالج التنبيهات - يرسل التنبيه للمتصلين"""
    message = {
        "type": "alert",
        "data": {
            "id": alert.id,
            "level": alert.level.value,
            "title": alert.title,
            "message": alert.message,
            "metric_type": alert.metric_type.value,
            "current_value": alert.current_value,
            "threshold": alert.threshold,
            "timestamp": alert.timestamp.isoformat(),
            "router_id": alert.router_id
        }
    }
    
    await connection_manager.broadcast(message)


# ==================== API Routes ====================

@app.get("/")
async def root():
    """نقطة البداية"""
    return {
        "message": "🧠 AI-Powered MikroTik Management Platform",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """فحص صحة النظام"""
    system_status = {
        "status": "healthy",
        "components": {
            "ai_brain": ai_brain is not None,
            "executor": executor is not None,
            "monitor": monitor is not None,
            "websocket_connections": len(connection_manager.active_connections)
        },
        "timestamp": datetime.now().isoformat()
    }
    
    if monitor and monitor.router_health:
        system_status["router_health"] = {
            "status": monitor.router_health.status,
            "health_score": monitor.router_health.health_score,
            "cpu_usage": monitor.router_health.cpu_usage,
            "memory_usage": monitor.router_health.memory_usage,
            "active_connections": monitor.router_health.active_connections
        }
    
    return system_status


@app.get("/api/status")
async def get_status():
    """الحصول على حالة النظام الكاملة"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    return {
        "system": {
            "ai_brain": ai_brain.get_status() if ai_brain else None,
            "executor": {
                "connected": executor is not None,
                "executions_count": len(executor.execution_history) if executor else 0
            },
            "monitor": monitor.get_current_status()
        },
        "router_health": monitor.router_health.__dict__ if monitor.router_health else None,
        "metrics_summary": monitor.get_metrics_summary(),
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/chat")
async def chat_with_ai(request: dict):
    """
    التحدث مع الذكاء الصناعي
    
    Body:
    {
        "message": "رسالة المستخدم",
        "user_role": "technician"
    }
    """
    if not ai_brain:
        raise HTTPException(status_code=503, detail="AI Brain not initialized")
    
    user_message = request.get("message", "")
    user_role = request.get("user_role", "technician")
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    # جمع سياق الشبكة الحالي
    network_context = None
    if monitor and monitor.router_health:
        health = monitor.router_health
        network_context = NetworkContext(
            router_ip=health.router_id,
            cpu_load=health.cpu_usage,
            memory_usage=health.memory_usage,
            active_connections=health.active_connections,
            bandwidth_usage={},
            interface_status={},
            recent_logs=[],
            alerts=[a.message for a in monitor.active_alerts.values() if not a.resolved]
        )
    
    # معالجة الرسالة
    try:
        decision = await ai_brain.process_natural_language(
            user_message=user_message,
            network_context=network_context,
            user_role=user_role
        )
        
        return {
            "success": True,
            "decision": {
                "intent": decision.intent.value,
                "confidence": decision.confidence,
                "action_plan": decision.action_plan,
                "reasoning": decision.reasoning,
                "mikrotik_script": decision.mikrotik_script,
                "rollback_plan": decision.rollback_plan,
                "risk_level": decision.risk_level,
                "requires_approval": decision.requires_approval,
                "estimated_execution_time": decision.estimated_execution_time,
                "model_used": decision.model_used,
                "timestamp": decision.timestamp.isoformat()
            }
        }
    
    except Exception as e:
        logger.error(f"خطأ في معالجة الرسالة: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/execute")
async def execute_script(request: dict):
    """
    تنفيذ سكربت على الراوتر
    
    Body:
    {
        "script": "سكربت MikroTik",
        "dry_run": true,
        "description": "وصف العملية"
    }
    """
    if not executor:
        raise HTTPException(status_code=503, detail="Executor not initialized")
    
    script = request.get("script", "")
    dry_run = request.get("dry_run", True)
    description = request.get("description", "")
    
    if not script:
        raise HTTPException(status_code=400, detail="Script is required")
    
    try:
        from engines.executor.routeros_executor import ExecutionMode
        
        mode = ExecutionMode.DRY_RUN if dry_run else ExecutionMode.SAFE
        
        result = await executor.execute(
            script=script,
            mode=mode,
            description=description
        )
        
        return {
            "success": result.success,
            "output": result.output,
            "error": result.error,
            "execution_time": result.execution_time,
            "commands_executed": result.commands_executed,
            "snapshot_id": result.snapshot_id,
            "rollback_available": result.rollback_available,
            "timestamp": result.timestamp.isoformat()
        }
    
    except Exception as e:
        logger.error(f"خطأ في التنفيذ: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics")
async def get_metrics():
    """الحصول على المقاييس الحالية"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    return monitor.get_metrics_summary()


@app.get("/api/alerts")
async def get_alerts():
    """الحصول على التنبيهات النشطة"""
    if not monitor:
        raise HTTPException(status_code=503, detail="Monitor not initialized")
    
    active_alerts = [
        {
            "id": alert.id,
            "level": alert.level.value,
            "title": alert.title,
            "message": alert.message,
            "metric_type": alert.metric_type.value,
            "current_value": alert.current_value,
            "threshold": alert.threshold,
            "timestamp": alert.timestamp.isoformat(),
            "resolved": alert.resolved
        }
        for alert in monitor.active_alerts.values()
    ]
    
    return {
        "count": len(active_alerts),
        "alerts": active_alerts
    }


@app.get("/api/ai/status")
async def get_ai_status():
    """الحصول على حالة الذكاء الصناعي"""
    if not ai_brain:
        raise HTTPException(status_code=503, detail="AI Brain not initialized")
    
    return ai_brain.get_status()


# ==================== WebSocket ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    نقطة اتصال WebSocket للتواصل الحي
    
    يرسل:
    - تحديثات المقاييس
    - التنبيهات الفورية
    - استجابات الذكاء الصناعي
    """
    await connection_manager.connect(websocket)
    
    try:
        # إرسال رسالة ترحيب
        await connection_manager.send_personal_message({
            "type": "welcome",
            "message": "مرحباً بك في منصة إدارة MikroTik الذكية!",
            "timestamp": datetime.now().isoformat()
        }, websocket)
        
        # حلقة استقبال الرسائل
        while True:
            # استقبال رسالة من العميل
            data = await websocket.receive_json()
            
            message_type = data.get("type")
            
            if message_type == "ping":
                # الرد على ping
                await connection_manager.send_personal_message({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }, websocket)
            
            elif message_type == "chat":
                # معالجة رسالة محادثة
                user_message = data.get("message", "")
                
                if ai_brain:
                    # معالجة الرسالة
                    decision = await ai_brain.process_natural_language(
                        user_message=user_message,
                        network_context=None,
                        user_role="technician"
                    )
                    
                    # إرسال الرد
                    await connection_manager.send_personal_message({
                        "type": "chat_response",
                        "decision": {
                            "intent": decision.intent.value,
                            "confidence": decision.confidence,
                            "action_plan": decision.action_plan,
                            "reasoning": decision.reasoning,
                            "mikrotik_script": decision.mikrotik_script,
                            "risk_level": decision.risk_level
                        },
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
            
            elif message_type == "get_status":
                # إرسال الحالة الحالية
                if monitor:
                    await connection_manager.send_personal_message({
                        "type": "status_update",
                        "data": monitor.get_current_status(),
                        "timestamp": datetime.now().isoformat()
                    }, websocket)
    
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"خطأ في WebSocket: {e}")
        connection_manager.disconnect(websocket)


# ==================== Background Tasks ====================

@app.on_event("startup")
async def startup_event():
    """عند بدء التشغيل"""
    # بدء مهمة بث المقاييس
    asyncio.create_task(broadcast_metrics_periodically())


async def broadcast_metrics_periodically():
    """بث المقاييس بشكل دوري لجميع المتصلين"""
    while True:
        try:
            await asyncio.sleep(5)  # كل 5 ثوان
            
            if monitor and len(connection_manager.active_connections) > 0:
                metrics_summary = monitor.get_metrics_summary()
                
                message = {
                    "type": "metrics_update",
                    "data": metrics_summary,
                    "timestamp": datetime.now().isoformat()
                }
                
                await connection_manager.broadcast(message)
        
        except Exception as e:
            logger.error(f"خطأ في بث المقاييس: {e}")


# ==================== Error Handlers ====================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """معالج أخطاء عام"""
    logger.error(f"خطأ غير متوقع: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 تشغيل خادم FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
