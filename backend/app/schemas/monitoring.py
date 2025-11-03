from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class InterfaceMetric(BaseModel):
    name: str
    rx_rate: float
    tx_rate: float
    status: str


class DeviceMetric(BaseModel):
    host: str
    cpu_load: float
    memory_usage: float
    uptime: float
    active_users: int
    packet_loss: float
    latency: float
    interfaces: list[InterfaceMetric] = Field(default_factory=list)
    collected_at: datetime = Field(default_factory=datetime.utcnow)


class MonitoringSnapshot(BaseModel):
    devices: list[DeviceMetric]
    anomalies: list[str] = Field(default_factory=list)


class MonitoringSubscription(BaseModel):
    subscription_id: str
    hosts: list[str]
    interval_seconds: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
