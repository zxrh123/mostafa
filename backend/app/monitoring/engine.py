"""
Monitoring Engine - Real-time network monitoring and analysis
"""

import asyncio
from typing import Dict, List, Optional, AsyncGenerator
from datetime import datetime
import logging
from app.core.config import settings
from app.ai.brain import AIBrain
from app.mikrotik.connector import MikroTikConnector

logger = logging.getLogger(__name__)


class MonitoringEngine:
    """
    Real-time monitoring engine for MikroTik routers
    Monitors CPU, RAM, interfaces, latency, and packet loss
    """
    
    def __init__(self, ai_brain: Optional[AIBrain] = None):
        self.ai_brain = ai_brain
        self.running = False
        self.routers: Dict[str, MikroTikConnector] = {}
        self.monitoring_tasks: List[asyncio.Task] = []
        self.update_queue = asyncio.Queue()
        self.subscribers: List[asyncio.Queue] = []
        
    async def start(self):
        """Start monitoring engine"""
        if self.running:
            return
        
        self.running = True
        logger.info("?? Monitoring Engine started")
        
        # Start main monitoring loop
        asyncio.create_task(self._monitoring_loop())
        
        # Start alert processor
        asyncio.create_task(self._alert_processor())
    
    async def stop(self):
        """Stop monitoring engine"""
        self.running = False
        
        # Cancel all monitoring tasks
        for task in self.monitoring_tasks:
            task.cancel()
        
        await asyncio.gather(*self.monitoring_tasks, return_exceptions=True)
        
        logger.info("?? Monitoring Engine stopped")
    
    def is_running(self) -> bool:
        """Check if monitoring is running"""
        return self.running
    
    async def add_router(
        self,
        router_id: str,
        host: str,
        username: str,
        password: str,
        port: int = 8728
    ):
        """Add a router to monitoring"""
        try:
            connector = MikroTikConnector(host, username, password, port)
            await connector.connect()
            
            self.routers[router_id] = connector
            logger.info(f"? Router {router_id} added to monitoring")
            
        except Exception as e:
            logger.error(f"? Failed to add router {router_id}: {e}")
            raise
    
    async def remove_router(self, router_id: str):
        """Remove a router from monitoring"""
        if router_id in self.routers:
            connector = self.routers[router_id]
            await connector.disconnect()
            del self.routers[router_id]
            logger.info(f"??? Router {router_id} removed from monitoring")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                for router_id, connector in self.routers.items():
                    if not connector.is_connected():
                        try:
                            await connector.connect()
                        except Exception as e:
                            logger.error(f"Failed to reconnect router {router_id}: {e}")
                            continue
                    
                    # Collect monitoring data
                    data = await self._collect_router_data(router_id, connector)
                    
                    # Check for alerts
                    alerts = await self._check_alerts(router_id, data)
                    
                    # Create update
                    update = {
                        "type": "monitoring_update",
                        "router_id": router_id,
                        "timestamp": datetime.now().isoformat(),
                        "data": data,
                        "alerts": alerts
                    }
                    
                    # Broadcast to subscribers
                    await self._broadcast_update(update)
                    
                    # Add to queue for processing
                    await self.update_queue.put(update)
                
                # Wait for next interval
                await asyncio.sleep(settings.MONITORING_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)
    
    async def _collect_router_data(
        self,
        router_id: str,
        connector: MikroTikConnector
    ) -> Dict:
        """Collect monitoring data from router"""
        try:
            # Get system resources
            system_resource = await connector.execute_command("/system/resource/print")
            
            # Get interface statistics
            interfaces = await connector.execute_command("/interface/print")
            
            # Get active connections
            connections = await connector.execute_command("/ip/connection/print")
            
            # Calculate metrics
            cpu_load = float(system_resource.get("cpu-load", 0))
            free_memory = int(system_resource.get("free-memory", 0))
            total_memory = int(system_resource.get("total-memory", 0))
            memory_usage = ((total_memory - free_memory) / total_memory * 100) if total_memory > 0 else 0
            
            # Interface statistics
            interface_stats = []
            for interface in interfaces:
                interface_stats.append({
                    "name": interface.get("name", ""),
                    "type": interface.get("type", ""),
                    "rx_byte": int(interface.get("rx-byte", 0)),
                    "tx_byte": int(interface.get("tx-byte", 0)),
                    "rx_packet": int(interface.get("rx-packet", 0)),
                    "tx_packet": int(interface.get("tx-packet", 0)),
                    "running": interface.get("running", False)
                })
            
            return {
                "cpu_load": cpu_load,
                "memory_usage": memory_usage,
                "free_memory": free_memory,
                "total_memory": total_memory,
                "interfaces": interface_stats,
                "active_connections": len(connections) if isinstance(connections, list) else 0,
                "uptime": system_resource.get("uptime", "")
            }
            
        except Exception as e:
            logger.error(f"Error collecting data from router {router_id}: {e}")
            return {
                "cpu_load": 0,
                "memory_usage": 0,
                "interfaces": [],
                "error": str(e)
            }
    
    async def _check_alerts(self, router_id: str, data: Dict) -> List[Dict]:
        """Check for alert conditions"""
        alerts = []
        
        # CPU alert
        if data.get("cpu_load", 0) > settings.ALERT_THRESHOLD_CPU:
            alerts.append({
                "type": "high_cpu",
                "severity": "warning",
                "message": f"CPU usage is high: {data['cpu_load']:.1f}%",
                "value": data["cpu_load"]
            })
        
        # Memory alert
        if data.get("memory_usage", 0) > settings.ALERT_THRESHOLD_RAM:
            alerts.append({
                "type": "high_memory",
                "severity": "warning",
                "message": f"Memory usage is high: {data['memory_usage']:.1f}%",
                "value": data["memory_usage"]
            })
        
        # Interface down alert
        for interface in data.get("interfaces", []):
            if not interface.get("running", False):
                alerts.append({
                    "type": "interface_down",
                    "severity": "error",
                    "message": f"Interface {interface['name']} is down",
                    "interface": interface["name"]
                })
        
        # Send alerts to AI Brain for analysis
        if alerts and self.ai_brain:
            try:
                analysis = await self.ai_brain.analyze_network_data(data)
                for alert in alerts:
                    alert["ai_recommendations"] = analysis.get("recommendations", [])
            except Exception as e:
                logger.error(f"Error in AI analysis: {e}")
        
        return alerts
    
    async def _alert_processor(self):
        """Process alerts and trigger auto-heal if needed"""
        while self.running:
            try:
                update = await asyncio.wait_for(
                    self.update_queue.get(),
                    timeout=1.0
                )
                
                alerts = update.get("alerts", [])
                if alerts:
                    # Check if auto-heal should be triggered
                    for alert in alerts:
                        if alert.get("severity") == "error":
                            # Critical alert - consider auto-heal
                            logger.warning(f"Critical alert: {alert['message']}")
                            # TODO: Implement auto-heal logic
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in alert processor: {e}")
    
    async def _broadcast_update(self, update: Dict):
        """Broadcast update to all subscribers"""
        for subscriber in self.subscribers:
            try:
                await subscriber.put(update)
            except Exception as e:
                logger.error(f"Error broadcasting to subscriber: {e}")
    
    async def get_updates(self) -> AsyncGenerator[Dict, None]:
        """Get real-time monitoring updates"""
        queue = asyncio.Queue()
        self.subscribers.append(queue)
        
        try:
            while self.running:
                update = await queue.get()
                yield update
        finally:
            if queue in self.subscribers:
                self.subscribers.remove(queue)
    
    async def get_current_status(self, router_id: Optional[str] = None) -> Dict:
        """Get current status of router(s)"""
        if router_id:
            if router_id in self.routers:
                connector = self.routers[router_id]
                return await self._collect_router_data(router_id, connector)
            else:
                return {"error": "Router not found"}
        else:
            # Return status for all routers
            status = {}
            for router_id, connector in self.routers.items():
                status[router_id] = await self._collect_router_data(router_id, connector)
            return status
