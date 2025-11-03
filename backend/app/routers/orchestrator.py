from datetime import datetime

from fastapi import APIRouter

from ..schemas.orchestrator import AutomationToggle, PlaybookExecution


router = APIRouter(prefix="/orchestrator", tags=["Automation"])

_toggles: dict[str, AutomationToggle] = {
    "auto_execute": AutomationToggle(feature="auto_execute", enabled=False),
    "auto_heal": AutomationToggle(feature="auto_heal", enabled=True),
    "load_balance": AutomationToggle(feature="load_balance", enabled=True),
}


@router.get("/toggles", response_model=list[AutomationToggle])
async def list_toggles() -> list[AutomationToggle]:
    return list(_toggles.values())


@router.post("/toggles/{feature}", response_model=AutomationToggle)
async def set_toggle(feature: str, toggle: AutomationToggle) -> AutomationToggle:
    if feature != toggle.feature:
        raise ValueError("Feature mismatch")
    toggle.updated_at = datetime.utcnow()
    _toggles[feature] = toggle
    return toggle


@router.post("/playbooks/{name}", response_model=PlaybookExecution)
async def trigger_playbook(name: str) -> PlaybookExecution:
    return PlaybookExecution(
        playbook=name,
        status="queued",
        started_at=datetime.utcnow(),
        details={"message": "Playbook queued for execution"},
    )
