from fastapi import APIRouter, Depends, Query

from ..api.deps import get_ai_core_service
from ..schemas.monitoring import MonitoringSnapshot
from ..services.ai_core import AICoreService


router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


@router.get("/snapshot", response_model=MonitoringSnapshot)
async def fetch_snapshot(
    hosts: list[str] | None = Query(default=None),
    service: AICoreService = Depends(get_ai_core_service),
) -> MonitoringSnapshot:
    """Return real-time telemetry for requested RouterOS hosts."""

    return await service.monitoring.collect_snapshot(hosts=hosts)
