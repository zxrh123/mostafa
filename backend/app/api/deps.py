"""FastAPI dependency providers."""

from __future__ import annotations

from typing import Optional

from ..services.ai_core import AICoreService, build_ai_core

_ai_core_service: Optional[AICoreService] = None


async def get_ai_core_service() -> AICoreService:
    global _ai_core_service
    if _ai_core_service is None:
        _ai_core_service = await build_ai_core()
    return _ai_core_service
