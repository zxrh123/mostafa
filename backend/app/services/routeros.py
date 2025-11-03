"""RouterOS connection management and helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from loguru import logger

from ..core.settings import get_settings


try:  # pragma: no cover - optional dependency
    import librouteros
except Exception:  # pragma: no cover
    librouteros = None


@dataclass
class RouterOSCredentials:
    host: str
    username: str
    password: str
    port: int = 8728
    use_ssl: bool = False


class RouterOSClientPool:
    """Very small connection pool abstraction."""

    def __init__(self) -> None:
        self._clients: dict[str, Any] = {}
        self.settings = get_settings()

    async def get_client(self, host: str) -> Any:
        if host in self._clients:
            return self._clients[host]

        if librouteros is None:
            raise RuntimeError("librouteros not installed; install to enable live RouterOS control")

        credentials = RouterOSCredentials(
            host=host,
            username=self.settings.routeros_username or "",
            password=self.settings.routeros_password or "",
        )
        logger.info("Connecting to RouterOS host {}", host)
        api = librouteros.connect(
            host=credentials.host,
            username=credentials.username,
            password=credentials.password,
            port=credentials.port,
            use_ssl=credentials.use_ssl,
        )
        self._clients[host] = api
        return api

    async def close_all(self) -> None:
        for host, client in self._clients.items():
            try:
                client.close()
            except Exception as exc:  # pragma: no cover
                logger.warning("Failed closing RouterOS client {}: {}", host, exc)
        self._clients.clear()
