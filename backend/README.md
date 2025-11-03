## AI-Driven MikroTik Management Backend

This FastAPI service orchestrates the Core AI Brain, RouterOS execution layer, monitoring engines, and real-time notification channels for the intelligent MikroTik network management platform.

### Key Modules
- `app/core`: configuration management, logging, security policies
- `app/api`: API routers, dependency injection, websocket gateways
- `app/services`: AI orchestrator, RouterOS executor, monitoring pipelines, knowledge base crawler
- `app/models` & `app/schemas`: persistence models and Pydantic DTOs for Postgres
- `app/workers`: background schedulers for polling, auto-heal, and knowledge ingestion
- `app/utils`: helpers for caching, notifications, and audit logging

### Getting Started
1. Install dependencies (requires Python 3.11+):
   ```bash
   poetry install
   ```
2. Define environment variables in `.env` (see `app/core/settings.py` for reference).
3. Run the API:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

### Testing
```bash
poetry run pytest
```
