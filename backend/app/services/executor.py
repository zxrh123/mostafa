"""RouterOS execution and audit service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import uuid
from typing import Any

from loguru import logger

from ..core.settings import get_settings
from ..schemas.ai import AIExecutionResult
from .routeros import RouterOSClientPool


@dataclass
class ExecutionAuditRecord:
    audit_id: str
    script: str
    metadata: dict[str, Any]
    created_at: datetime
    executed: bool = False
    output_logs: list[str] | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None


class ExecutionAuditStore:
    def __init__(self) -> None:
        self._store: dict[str, ExecutionAuditRecord] = {}

    def create(self, script: str, metadata: dict[str, Any]) -> ExecutionAuditRecord:
        audit = ExecutionAuditRecord(
            audit_id=str(uuid.uuid4()),
            script=script,
            metadata=metadata,
            created_at=datetime.utcnow(),
        )
        self._store[audit.audit_id] = audit
        return audit

    def get(self, audit_id: str) -> ExecutionAuditRecord:
        try:
            return self._store[audit_id]
        except KeyError as exc:
            raise KeyError(f"Audit {audit_id} not found") from exc


class ExecutorService:
    def __init__(self, routeros_pool: RouterOSClientPool) -> None:
        self.routeros_pool = routeros_pool
        self.audit_store = ExecutionAuditStore()

    async def validate(self, script: str) -> bool:
        return script.strip().startswith("<script>") and script.strip().endswith("</script>")

    async def execute(self, script: str, metadata: dict[str, Any]) -> AIExecutionResult:
        audit = self.audit_store.create(script, metadata)
        audit.started_at = datetime.utcnow()
        audit.output_logs = []

        # Placeholder: actual RouterOS execution would use API.
        hosts = metadata.get("hosts") or get_settings().routeros_hosts
        audit.output_logs.append(f"Preparing execution on hosts: {hosts}")
        try:
            for host in hosts:
                client = await self.routeros_pool.get_client(host)
                # RouterOS scripts typically require removing <script> tags
                clean_script = script.replace("<script>", "").replace("</script>", "").strip()
                audit.output_logs.append(f"Executing on {host}: {clean_script[:60]}...")
                client(cmd="/cmd", script=clean_script)  # type: ignore[attr-defined]
        except Exception as exc:  # pragma: no cover
            logger.error("Execution failed: {}", exc)
            audit.output_logs.append(f"Execution error: {exc}")
            audit.executed = False
        else:
            audit.executed = True
            audit.output_logs.append("Execution completed successfully")

        audit.finished_at = datetime.utcnow()
        result = AIExecutionResult(
            audit_id=audit.audit_id,
            executed=audit.executed,
            output_logs=audit.output_logs or [],
            started_at=audit.started_at or audit.created_at,
            finished_at=audit.finished_at or datetime.utcnow(),
            rollback_available=False,
        )
        return result

    async def execute_from_audit(self, audit_id: str) -> AIExecutionResult:
        audit = self.audit_store.get(audit_id)
        return await self.execute(audit.script, audit.metadata)
