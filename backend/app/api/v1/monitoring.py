"""
Monitoring API
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, Dict, Any
from app.monitoring.engine import MonitoringEngine
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# This would be injected via dependency injection in production
monitoring_engine: Optional[MonitoringEngine] = None


def set_monitoring_engine(engine: MonitoringEngine):
    """Set monitoring engine instance"""
    global monitoring_engine
    monitoring_engine = engine


@router.get("/status")
async def get_monitoring_status():
    """Get monitoring engine status"""
    if not monitoring_engine:
        return {
            "status": "inactive",
            "running": False
        }
    
    return {
        "status": "active" if monitoring_engine.is_running() else "inactive",
        "running": monitoring_engine.is_running(),
        "routers_count": len(monitoring_engine.routers)
    }


@router.get("/routers/{router_id}")
async def get_router_status(router_id: str):
    """Get current status of a router"""
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    try:
        status = await monitoring_engine.get_current_status(router_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/routers")
async def get_all_routers_status():
    """Get status of all routers"""
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    try:
        status = await monitoring_engine.get_current_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
