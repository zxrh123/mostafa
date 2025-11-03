"""Core AI Brain orchestrator."""

from __future__ import annotations

import json
from typing import Any

import httpx
from loguru import logger

from ..core.settings import get_settings
from ..schemas.ai import AICommandRequest, AICommandResponse, AIExecutionResult, AIPlanStep
from .executor import ExecutorService
from .monitoring import MonitoringService
from .routeros import RouterOSClientPool


class GPTClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(timeout=30)

    async def chat(self, messages: list[dict[str, str]]) -> str:
        if not self.api_key:
            raise RuntimeError("OpenAI API key not configured")
        response = await self._client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
            },
            json={"model": self.model, "messages": messages},
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


class GeminiClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(timeout=30)

    async def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("Gemini API key not configured")
        response = await self._client.post(
            f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent",
            params={"key": self.api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


class AICoreService:
    def __init__(
        self,
        executor: ExecutorService,
        monitoring: MonitoringService,
        routeros_pool: RouterOSClientPool,
    ) -> None:
        settings = get_settings()
        self.executor = executor
        self.monitoring = monitoring
        self.routeros_pool = routeros_pool
        self.gpt = GPTClient(settings.openai_api_key or "", settings.openai_model)
        self.gemini = GeminiClient(settings.gemini_api_key or "", settings.gemini_model)

    async def _analyze_intent(self, request: AICommandRequest) -> dict[str, Any]:
        prompt = (
            "You are the Core AI Brain of a MikroTik network control plane. "
            "Analyze the following user message and output JSON with keys intent, confidence, "
            "and reasoning."
            f"\nMessage: {request.message}\nContext: {request.context}"
        )
        try:
            response = await self.gpt.chat(
                [
                    {"role": "system", "content": "You respond strictly with JSON."},
                    {"role": "user", "content": prompt},
                ]
            )
        except Exception as exc:  # pragma: no cover - network failure fallback
            logger.warning("GPT intent analysis failed: {}", exc)
            raise
        try:
            return json.loads(response)
        except json.JSONDecodeError as exc:
            logger.error("Intent analysis returned non-JSON payload: {}", response)
            raise RuntimeError("Invalid intent payload") from exc

    async def _generate_plan(self, intent_payload: dict[str, Any], request: AICommandRequest) -> list[AIPlanStep]:
        prompt = (
            "Draft an execution plan (max 5 steps) for the MikroTik control plane based on the intent."
            f"\nIntent payload: {intent_payload}\nUser message: {request.message}"
        )
        try:
            response = await self.gemini.generate(prompt)
        except Exception as exc:  # pragma: no cover
            logger.warning("Gemini plan generation failed: {}", exc)
            raise

        # naive parsing fallback: expect bullet list
        steps: list[AIPlanStep] = []
        for order, line in enumerate(response.splitlines(), start=1):
            cleaned = line.strip("- ")
            if cleaned:
                steps.append(AIPlanStep(order=order, action=cleaned.split(":")[0], description=cleaned))
        return steps

    async def _generate_script(self, request: AICommandRequest, intent_payload: dict[str, Any]) -> str:
        prompt = (
            "Generate a MikroTik RouterOS script. Always wrap the output in <script> tags. "
            "Do not include explanations.\n"
            f"Intent: {intent_payload}\nUser message: {request.message}\n"
        )
        response = await self.gpt.chat(
            [
                {"role": "system", "content": "Output RouterOS script only."},
                {"role": "user", "content": prompt},
            ]
        )
        return response

    async def process(self, request: AICommandRequest) -> AICommandResponse:
        intent_payload = await self._analyze_intent(request)
        plan = await self._generate_plan(intent_payload, request)
        script = await self._generate_script(request, intent_payload)

        response = AICommandResponse(
            conversation_id=request.conversation_id,
            intent=intent_payload.get("intent", "unknown"),
            confidence=float(intent_payload.get("confidence", 0.0)),
            plan=plan,
            generated_script=script,
            validation_passed=False,
            executed=False,
        )

        validation = await self.executor.validate(script)
        response.validation_passed = validation
        if validation and request.context and request.context.get("auto_execute"):
            exec_result = await self.executor.execute(script, metadata={"conversation_id": request.conversation_id})
            response.executed = exec_result.executed
            response.audit_id = exec_result.audit_id
        return response

    async def execute(self, audit_id: str) -> AIExecutionResult:
        return await self.executor.execute_from_audit(audit_id)


async def build_ai_core() -> AICoreService:
    executor = ExecutorService(routeros_pool=RouterOSClientPool())
    monitoring = MonitoringService(routeros_pool=executor.routeros_pool)
    return AICoreService(executor=executor, monitoring=monitoring, routeros_pool=executor.routeros_pool)
