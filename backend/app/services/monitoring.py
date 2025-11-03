"""Live network telemetry collector."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from loguru import logger

from ..core.settings import get_settings
from ..schemas.monitoring import DeviceMetric, InterfaceMetric, MonitoringSnapshot, MonitoringSubscription
from .routeros import RouterOSClientPool


class MonitoringService:
    def __init__(self, routeros_pool: RouterOSClientPool) -> None:
        self.routeros_pool = routeros_pool
        self.settings = get_settings()
        self._subscriptions: dict[str, MonitoringSubscription] = {}

    async def collect_snapshot(self, hosts: list[str] | None = None) -> MonitoringSnapshot:
        hosts = hosts or [str(url) for url in self.settings.routeros_hosts]
        devices: list[DeviceMetric] = []
        for host in hosts:
            try:
                client = await self.routeros_pool.get_client(host)
                metrics = await self._collect_from_router(client)
                devices.append(metrics)
            except Exception as exc:  # pragma: no cover
                logger.warning("Failed to collect metrics for {}: {}", host, exc)
        anomalies = self._detect_anomalies(devices)
        return MonitoringSnapshot(devices=devices, anomalies=anomalies)

    async def _collect_from_router(self, client: Any) -> DeviceMetric:
        # TODO: replace with direct RouterOS API commands (/system/resource/print etc.)
        interfaces = [
            InterfaceMetric(name="ether1", rx_rate=random.uniform(10, 100), tx_rate=random.uniform(5, 80), status="up"),
            InterfaceMetric(name="wlan1", rx_rate=random.uniform(1, 50), tx_rate=random.uniform(1, 50), status="up"),
        ]
        metric = DeviceMetric(
            host=str(client.host) if hasattr(client, "host") else "mock-host",
            cpu_load=random.uniform(5, 90),
            memory_usage=random.uniform(10, 90),
            uptime=random.uniform(1000, 500000),
            active_users=random.randint(1, 500),
            packet_loss=random.uniform(0, 10),
            latency=random.uniform(1, 200),
            interfaces=interfaces,
            collected_at=datetime.utcnow(),
        )
        return metric

    def _detect_anomalies(self, devices: list[DeviceMetric]) -> list[str]:
        anomalies: list[str] = []
        for device in devices:
            if device.cpu_load > 85:
                anomalies.append(f"High CPU load on {device.host}: {device.cpu_load:.1f}%")
            if device.packet_loss > 5:
                anomalies.append(f"Packet loss on {device.host}: {device.packet_loss:.1f}%")
            for iface in device.interfaces:
                if iface.status != "up":
                    anomalies.append(f"Interface {iface.name} down on {device.host}")
        return anomalies

    async def subscribe(self, subscription: MonitoringSubscription) -> None:
        self._subscriptions[subscription.subscription_id] = subscription
        logger.info("Registered monitoring subscription {}", subscription.subscription_id)

    async def unsubscribe(self, subscription_id: str) -> None:
        self._subscriptions.pop(subscription_id, None)
        logger.info("Removed monitoring subscription {}", subscription_id)
