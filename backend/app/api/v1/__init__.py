"""
API v1 Routes
"""

from fastapi import APIRouter
from app.api.v1 import routers, monitoring, execution, chat

router = APIRouter()

# Include sub-routers
router.include_router(routers.router, prefix="/routers", tags=["routers"])
router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
router.include_router(execution.router, prefix="/execution", tags=["execution"])
router.include_router(chat.router, prefix="/chat", tags=["chat"])
