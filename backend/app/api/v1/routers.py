"""
Router Management API
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from app.monitoring.engine import MonitoringEngine
from app.mikrotik.connector import MikroTikConnector
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class RouterCreate(BaseModel):
    router_id: str
    name: str
    host: str
    username: str
    password: str
    api_port: int = 8728
    ssh_port: int = 22


class RouterResponse(BaseModel):
    router_id: str
    name: str
    host: str
    is_connected: bool
    last_seen: Optional[str] = None


# This would be injected via dependency injection in production
monitoring_engine: Optional[MonitoringEngine] = None


def set_monitoring_engine(engine: MonitoringEngine):
    """Set monitoring engine instance"""
    global monitoring_engine
    monitoring_engine = engine


@router.post("/", response_model=RouterResponse)
async def add_router(router_data: RouterCreate):
    """Add a router to the system"""
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    try:
        await monitoring_engine.add_router(
            router_id=router_data.router_id,
            host=router_data.host,
            username=router_data.username,
            password=router_data.password,
            port=router_data.api_port
        )
        
        return RouterResponse(
            router_id=router_data.router_id,
            name=router_data.name,
            host=router_data.host,
            is_connected=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[RouterResponse])
async def list_routers():
    """List all routers"""
    if not monitoring_engine:
        return []
    
    routers = []
    for router_id, connector in monitoring_engine.routers.items():
        routers.append(RouterResponse(
            router_id=router_id,
            name=router_id,  # Would come from database
            host=connector.host,
            is_connected=connector.is_connected()
        ))
    
    return routers


@router.get("/{router_id}", response_model=RouterResponse)
async def get_router(router_id: str):
    """Get router details"""
    if not monitoring_engine or router_id not in monitoring_engine.routers:
        raise HTTPException(status_code=404, detail="Router not found")
    
    connector = monitoring_engine.routers[router_id]
    return RouterResponse(
        router_id=router_id,
        name=router_id,
        host=connector.host,
        is_connected=connector.is_connected()
    )


@router.delete("/{router_id}")
async def remove_router(router_id: str):
    """Remove a router from monitoring"""
    if not monitoring_engine:
        raise HTTPException(status_code=503, detail="Monitoring engine not available")
    
    try:
        await monitoring_engine.remove_router(router_id)
        return {"status": "success", "message": f"Router {router_id} removed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
