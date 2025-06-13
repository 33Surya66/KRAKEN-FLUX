import asyncio
import logging
import psutil
from datetime import datetime
from typing import Dict, List, Optional

from ..core.agent_types import AgentType, AgentCapability
from ..models.database import SystemMetrics
from ..core.database import db_manager

logger = logging.getLogger(__name__)

class MonitoringAgent:
    def __init__(self, agent_id: str, configuration: Dict):
        self.agent_id = agent_id
        self.configuration = configuration
        self._running = False
        self._last_metrics: Optional[Dict] = None

    async def start(self):
        """Start the monitoring agent."""
        self._running = True
        logger.info(f"Monitoring agent {self.agent_id} started")

    async def stop(self):
        """Stop the monitoring agent."""
        self._running = False
        logger.info(f"Monitoring agent {self.agent_id} stopped")

    async def collect_system_metrics(self) -> Dict:
        """Collect system metrics."""
        try:
            metrics = {
                "timestamp": datetime.utcnow(),
                "cpu": {
                    "percent": psutil.cpu_percent(interval=1),
                    "count": psutil.cpu_count(),
                    "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
                },
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent
                },
                "disk": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free,
                    "percent": psutil.disk_usage('/').percent
                },
                "network": {
                    "bytes_sent": psutil.net_io_counters().bytes_sent,
                    "bytes_recv": psutil.net_io_counters().bytes_recv,
                    "packets_sent": psutil.net_io_counters().packets_sent,
                    "packets_recv": psutil.net_io_counters().packets_recv
                }
            }
            return metrics
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return {}

    async def analyze_metrics(self, metrics: Dict) -> List[Dict]:
        """Analyze collected metrics for potential issues."""
        alerts = []
        
        # CPU usage alert
        if metrics.get("cpu", {}).get("percent", 0) > self.configuration.get("alert_threshold", 80):
            alerts.append({
                "type": "high_cpu_usage",
                "severity": "warning",
                "message": f"High CPU usage detected: {metrics['cpu']['percent']}%"
            })

        # Memory usage alert
        if metrics.get("memory", {}).get("percent", 0) > self.configuration.get("alert_threshold", 80):
            alerts.append({
                "type": "high_memory_usage",
                "severity": "warning",
                "message": f"High memory usage detected: {metrics['memory']['percent']}%"
            })

        # Disk usage alert
        if metrics.get("disk", {}).get("percent", 0) > self.configuration.get("alert_threshold", 80):
            alerts.append({
                "type": "high_disk_usage",
                "severity": "warning",
                "message": f"High disk usage detected: {metrics['disk']['percent']}%"
            })

        return alerts

    async def store_metrics(self, metrics: Dict):
        """Store collected metrics in the database."""
        try:
            async with db_manager.get_session() as session:
                system_metrics = SystemMetrics(
                    agent_id=self.agent_id,
                    metric_type="system",
                    metrics_data=metrics,
                    timestamp=metrics["timestamp"]
                )
                session.add(system_metrics)
                await session.commit()
        except Exception as e:
            logger.error(f"Error storing system metrics: {str(e)}")

    async def run(self):
        """Main monitoring loop."""
        try:
            while self._running:
                # Collect metrics
                metrics = await self.collect_system_metrics()
                
                # Analyze metrics
                alerts = await self.analyze_metrics(metrics)
                
                # Store metrics
                await self.store_metrics(metrics)
                
                # Process alerts
                for alert in alerts:
                    logger.warning(f"Alert: {alert['message']}")
                    # TODO: Implement alert handling
                
                # Store last metrics for comparison
                self._last_metrics = metrics
                
                # Sleep for the configured interval
                await asyncio.sleep(self.configuration.get("interval", 30))
        except Exception as e:
            logger.error(f"Error in monitoring agent loop: {str(e)}")
            await self.stop() 