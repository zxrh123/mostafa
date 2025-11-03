# MikroTik AI Control Plane Architecture

## Core Pillars
- **AI Orchestration**: `app/services/ai_core.py` merges OpenAI GPT (strategic reasoning, script generation) with Google Gemini (fast planning, data summarisation) via asynchronous clients.
- **Network Control**: `RouterOSClientPool` manages authenticated MikroTik sessions; `ExecutorService` performs dry-run validation, script dispatch, and audit log capture.
- **Monitoring**: `MonitoringService` aggregates CPU, RAM, interface metrics, and anomaly detection; periodic jobs run through `workers/scheduler.py`.
- **Knowledge Intelligence**: `knowledge_base/crawler.py` ingests MikroTik community content for continuous knowledge updates.
- **Front-End Experience**: React + Tailwind dashboard (`frontend/src/pages`) with dark glassmorphism visuals, Framer Motion transitions, and a bidirectional AI assistant widget.

## Service Topology
- **FastAPI Backend** (`backend/app`)
  - `/api/v1/ai`: intent processing, plan generation, executor trigger
  - `/api/v1/monitoring`: live telemetry snapshots
  - `/api/v1/network`: host inventory + direct command channel
  - `/api/v1/orchestrator`: automation toggles, playbook dispatch
  - `/ws/ai`: WebSocket gateway for real-time AI assistant updates
- **Datastores** (expected)
  - PostgreSQL: operational data, execution audits, knowledge index
  - Redis: pub/sub for notifications, caching
- **Background Workers**
  - APScheduler tasks for telemetry polling, auto-heal cycles, knowledge refresh

## Execution Flow
1. Operator/customer issues natural-language instruction (UI chat widget or API).
2. `AICoreService` analyses intent (GPT), drafts micro-plan (Gemini), produces RouterOS script.
3. `ExecutorService` validates syntax (dry-run) then issues commands across targeted routers, storing audit trail.
4. Monitoring engine observes impact, anomalies trigger notifications via WebSocket/UI.
5. Knowledge base updated with execution context and outcomes.

## Security & Safety Controls
- Configurable `auto_execute` toggle; default `false`.
- Snapshot policy enforced via scheduled tasks; rollback hooks prepared.
- Audit logs persisted through Loguru JSON sink (`audit.log`).
- Role-based access to endpoints (JWT scaffolding placeholder in `core/settings`).

## Front-End Highlights
- Animated dashboard cards (`MetricCard`), pseudo real-time charts (`RealtimeTrend`), AI assistant (`AIChatWidget`).
- Arabic-first interface using Unicode escapes to maintain ASCII source compliance.
- Proxy configuration in `vite.config.ts` for local FastAPI integration.

## Next-Steps Checklist
- Implement concrete RouterOS dry-run (using `/system/script/print` w/ `parse-only`).
- Wire PostgreSQL models + Alembic migrations for audits, telemetry, toggles.
- Integrate Redis Pub/Sub for pushing anomaly events to WebSocket clients.
- Replace mocked monitoring data with actual RouterOS metrics consumption.
- Harden AI connectors with rate limiting, error translation, and caching.
- Add unit/integration tests (`pytest`, `pytest-asyncio`).
