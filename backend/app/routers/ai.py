from fastapi import APIRouter, Depends, HTTPException, status

from ..api.deps import get_ai_core_service
from ..schemas.ai import AICommandRequest, AICommandResponse, AIExecutionResult
from ..services.ai_core import AICoreService


router = APIRouter(prefix="/ai", tags=["AI Brain"])


@router.post("/command", response_model=AICommandResponse)
async def process_command(
    payload: AICommandRequest,
    service: AICoreService = Depends(get_ai_core_service),
) -> AICommandResponse:
    """Analyse an instruction and produce an execution plan."""

    return await service.process(payload)


@router.post("/audit/{audit_id}/execute", response_model=AIExecutionResult)
async def execute_from_audit(
    audit_id: str,
    service: AICoreService = Depends(get_ai_core_service),
) -> AIExecutionResult:
    try:
        return await service.execute(audit_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
