"""Background scheduler for monitoring and auto-heal jobs."""

from __future__ import annotations

from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from ..api.deps import get_ai_core_service


scheduler = AsyncIOScheduler()


async def refresh_monitoring_snapshot() -> None:
    service = await get_ai_core_service()
    snapshot = await service.monitoring.collect_snapshot()
    logger.debug("Monitoring snapshot broadcasted: {} devices", len(snapshot.devices))


async def auto_heal_cycle() -> None:
    logger.debug("Auto-heal cycle triggered (implement remediation logic)")


@asynccontextmanager
async def scheduler_lifespan():
    scheduler.add_job(refresh_monitoring_snapshot, trigger="interval", seconds=30, id="monitoring")
    scheduler.add_job(auto_heal_cycle, trigger="interval", seconds=120, id="auto_heal")
    scheduler.start()
    logger.info("Background scheduler started")
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)
        logger.info("Background scheduler stopped")
