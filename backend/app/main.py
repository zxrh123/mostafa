"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.logging import setup_logging
from .core.settings import get_settings
from .routers import ai, monitoring, network, orchestrator, websocket
from .workers.scheduler import scheduler_lifespan


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    async with scheduler_lifespan():
        yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.project_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ai.router, prefix=settings.api_v1_prefix)
    app.include_router(network.router, prefix=settings.api_v1_prefix)
    app.include_router(monitoring.router, prefix=settings.api_v1_prefix)
    app.include_router(orchestrator.router, prefix=settings.api_v1_prefix)
    app.include_router(websocket.router)

    return app


app = create_app()
