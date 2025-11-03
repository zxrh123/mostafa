"""
MikroTik AI Management Platform - Main Application
Core AI Brain Integration with FastAPI
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import router as api_router
from app.websocket.manager import ConnectionManager
from app.ai.brain import AIBrain
from app.monitoring.engine import MonitoringEngine
from app.executor.engine import ExecutorEngine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global instances
ai_brain: AIBrain = None
monitoring_engine: MonitoringEngine = None
executor_engine: ExecutorEngine = None
ws_manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global ai_brain, monitoring_engine, executor_engine
    
    logger.info("?? Starting MikroTik AI Management Platform...")
    
    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize Core AI Brain
    logger.info("?? Initializing Core AI Brain...")
    ai_brain = AIBrain()
    await ai_brain.initialize()
    
    # Initialize Monitoring Engine
    logger.info("?? Starting Monitoring Engine...")
    monitoring_engine = MonitoringEngine(ai_brain=ai_brain)
    await monitoring_engine.start()
    
    # Initialize Executor Engine
    logger.info("?? Initializing Executor Engine...")
    executor_engine = ExecutorEngine(ai_brain=ai_brain)
    
    # Inject engines into API routes
    from app.api.v1 import routers, monitoring, execution, chat
    routers.set_monitoring_engine(monitoring_engine)
    monitoring.set_monitoring_engine(monitoring_engine)
    execution.set_executor_engine(executor_engine)
    execution.set_monitoring_engine(monitoring_engine)
    chat.set_ai_brain(ai_brain)
    
    logger.info("? System initialized successfully!")
    
    yield
    
    # Cleanup
    logger.info("?? Shutting down...")
    if monitoring_engine:
        await monitoring_engine.stop()
    if ai_brain:
        await ai_brain.cleanup()


# Create FastAPI app
app = FastAPI(
    title="MikroTik AI Management Platform",
    description="AI-Powered Network Management System with Core AI Brain",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "status": "online",
        "platform": "MikroTik AI Management Platform",
        "version": "1.0.0",
        "ai_brain": "active" if ai_brain else "initializing",
        "monitoring": "active" if monitoring_engine else "inactive"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "ai_brain": ai_brain.is_ready() if ai_brain else False,
            "monitoring": monitoring_engine.is_running() if monitoring_engine else False,
            "executor": executor_engine.is_ready() if executor_engine else False
        }
    }


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for AI Chat"""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            user_id = data.get("user_id", "anonymous")
            
            if not user_message:
                continue
            
            # Send to AI Brain for processing
            if ai_brain:
                response = await ai_brain.process_chat_message(
                    message=user_message,
                    user_id=user_id,
                    context=data.get("context", {})
                )
                
                await ws_manager.send_personal_message({
                    "type": "ai_response",
                    "message": response["message"],
                    "actions": response.get("actions", []),
                    "confidence": response.get("confidence", 0.0)
                }, websocket)
            else:
                await ws_manager.send_personal_message({
                    "type": "error",
                    "message": "AI Brain is not ready yet"
                }, websocket)
                
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@app.websocket("/ws/monitoring")
async def websocket_monitoring(websocket: WebSocket):
    """WebSocket endpoint for real-time monitoring data"""
    await ws_manager.connect(websocket)
    try:
        if monitoring_engine:
            # Subscribe to monitoring updates
            async for update in monitoring_engine.get_updates():
                await ws_manager.send_personal_message(update, websocket)
        else:
            await ws_manager.send_personal_message({
                "type": "error",
                "message": "Monitoring engine is not available"
            }, websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
