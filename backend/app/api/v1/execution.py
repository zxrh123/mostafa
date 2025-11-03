"""
Execution API
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.executor.engine import ExecutorEngine
from app.monitoring.engine import MonitoringEngine
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# This would be injected via dependency injection in production
executor_engine: Optional[ExecutorEngine] = None
monitoring_engine: Optional[MonitoringEngine] = None


def set_executor_engine(engine: ExecutorEngine):
    """Set executor engine instance"""
    global executor_engine
    executor_engine = engine


def set_monitoring_engine(engine: MonitoringEngine):
    """Set monitoring engine instance"""
    global monitoring_engine
    monitoring_engine = engine


class ExecuteScriptRequest(BaseModel):
    router_id: str
    script: str
    dry_run: bool = True
    require_confirmation: bool = True
    user_id: Optional[str] = None


class ExecuteAIRequest(BaseModel):
    router_id: str
    message: str
    user_id: Optional[str] = None


@router.post("/script")
async def execute_script(request: ExecuteScriptRequest):
    """Execute a RouterOS script"""
    if not executor_engine:
        raise HTTPException(status_code=503, detail="Executor engine not available")
    
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    if request.router_id not in monitoring_engine.routers:
        raise HTTPException(status_code=404, detail="Router not found")
    
    connector = monitoring_engine.routers[request.router_id]
    
    try:
        result = await executor_engine.execute_script(
            router_id=request.router_id,
            script=request.script,
            connector=connector,
            dry_run=request.dry_run,
            require_confirmation=request.require_confirmation,
            user_id=request.user_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ai")
async def execute_with_ai(request: ExecuteAIRequest):
    """Execute command using AI based on natural language"""
    if not executor_engine:
        raise HTTPException(status_code=503, detail="Executor engine not available")
    
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    if request.router_id not in monitoring_engine.routers:
        raise HTTPException(status_code=404, detail="Router not found")
    
    connector = monitoring_engine.routers[request.router_id]
    
    try:
        result = await executor_engine.execute_with_ai(
            router_id=request.router_id,
            user_message=request.message,
            connector=connector,
            user_id=request.user_id
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history/{router_id}")
async def get_execution_history(router_id: str, limit: int = 100):
    """Get execution history for a router"""
    if not executor_engine:
        raise HTTPException(status_code=503, detail="Executor engine not available")
    
    try:
        history = await executor_engine.get_execution_history(router_id, limit)
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rollback/{execution_id}")
async def rollback_execution(execution_id: str, router_id: str):
    """Rollback to a previous execution snapshot"""
    if not executor_engine:
        raise HTTPException(status_code=503, detail="Executor engine not available")
    
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    if router_id not in monitoring_engine.routers:
        raise HTTPException(status_code=404, detail="Router not found")
    
    connector = monitoring_engine.routers[router_id]
    
    try:
        result = await executor_engine.rollback(execution_id, router_id, connector)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
