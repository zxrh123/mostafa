from datetime import datetime

from pydantic import BaseModel, Field


class AutomationToggle(BaseModel):
    feature: str
    enabled: bool
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PlaybookExecution(BaseModel):
    playbook: str
    status: str
    started_at: datetime
    finished_at: datetime | None = None
    details: dict[str, str] = Field(default_factory=dict)
