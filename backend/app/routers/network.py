from fastapi import APIRouter, Depends, HTTPException, status

from ..api.deps import get_ai_core_service
from ..core.settings import get_settings
from ..schemas.network import RouterCommand
from ..services.ai_core import AICoreService


router = APIRouter(prefix="/network", tags=["RouterOS"])


@router.get("/hosts", response_model=list[str])
async def list_hosts() -> list[str]:
    settings = get_settings()
    return [str(host) for host in settings.routeros_hosts]


@router.post("/command")
async def run_command(
    payload: RouterCommand,
    service: AICoreService = Depends(get_ai_core_service),
) -> dict[str, str]:
    if payload.dry_run:
        return {"status": "dry-run", "command": payload.command}

    try:
        client = await service.routeros_pool.get_client(payload.host)
        client(cmd=payload.command)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    return {"status": "executed"}
