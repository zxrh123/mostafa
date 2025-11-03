from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class AICommandRequest(BaseModel):
    conversation_id: str = Field(..., description="Unique conversation identifier")
    sender: str = Field(..., description="Origin of the request: operator, customer, system")
    message: str = Field(..., description="Natural language instruction or question")
    context: dict[str, Any] | None = Field(default=None, description="Extra telemetry or session info")


class AIPlanStep(BaseModel):
    order: int
    action: str
    description: str


class AICommandResponse(BaseModel):
    conversation_id: str
    intent: str
    confidence: float
    plan: list[AIPlanStep]
    generated_script: str | None = None
    validation_passed: bool = False
    executed: bool = False
    audit_id: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AIExecutionResult(BaseModel):
    audit_id: str
    executed: bool
    output_logs: list[str]
    started_at: datetime
    finished_at: datetime
    rollback_available: bool = False


class AIRecommendation(BaseModel):
    summary: str
    impact_score: float
    actions: list[str]
