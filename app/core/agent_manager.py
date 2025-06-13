from typing import Dict, List, Optional, Type
import asyncio
import logging
from datetime import datetime
from ..models.database import Agent as AgentModel
from ..core.database import db_manager

from ..agents.base_agent import BaseAgent
from ..agents.guardian_agent import GuardianAgent
from ..agents.forensic_agent import ForensicAgent
from ..agents.containment_agent import ContainmentAgent
from ..agents.compliance_agent import ComplianceAgent
from ..agents.simulation_agent import SimulationAgent

logger = logging.getLogger(__name__)

class AgentManager:
    """Manages and coordinates all KRAKEN-FLUX agents."""
    
    def __init__(self):
        self.active_agents: Dict[str, Dict] = {}
        self.agent_tasks: Dict[str, asyncio.Task] = {}
        self._initialized = False
        self.logger = logging.getLogger("AgentManager")
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_types: Dict[str, Type[BaseAgent]] = {
            "guardian": GuardianAgent,
            "forensic": ForensicAgent,
            "containment": ContainmentAgent,
            "compliance": ComplianceAgent,
            "simulation": SimulationAgent
        }
        
    async def initialize(self) -> bool:
        """Initialize the agent manager and load existing agents."""
        try:
            if self._initialized:
                return True

            # Load existing agents from database
            async with db_manager.get_session() as session:
                agents = await session.query(AgentModel).all()
                for agent in agents:
                    if agent.status == "active":
                        await self.start_agent(agent)

            self._initialized = True
            logger.info("Agent manager initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing agent manager: {str(e)}")
            return False

    async def start_agent(self, agent: AgentModel) -> bool:
        """Start an agent and its associated tasks."""
        try:
            if agent.id in self.active_agents:
                logger.warning(f"Agent {agent.id} is already running")
                return False

            # Create agent task
            task = asyncio.create_task(self._run_agent(agent))
            self.agent_tasks[agent.id] = task
            self.active_agents[agent.id] = {
                "agent": agent,
                "started_at": datetime.utcnow(),
                "last_heartbeat": datetime.utcnow()
            }

            logger.info(f"Agent {agent.id} started successfully")
            return True
        except Exception as e:
            logger.error(f"Error starting agent {agent.id}: {str(e)}")
            return False

    async def stop_agent(self, agent_id: str) -> bool:
        """Stop an agent and its associated tasks."""
        try:
            if agent_id not in self.active_agents:
                logger.warning(f"Agent {agent_id} is not running")
                return False

            # Cancel agent task
            task = self.agent_tasks.get(agent_id)
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            # Remove agent from active agents
            del self.active_agents[agent_id]
            del self.agent_tasks[agent_id]

            logger.info(f"Agent {agent_id} stopped successfully")
            return True
        except Exception as e:
            logger.error(f"Error stopping agent {agent_id}: {str(e)}")
            return False

    async def _run_agent(self, agent: AgentModel):
        """Run the agent's main loop."""
        try:
            while True:
                # Update agent heartbeat
                self.active_agents[agent.id]["last_heartbeat"] = datetime.utcnow()

                # Execute agent's capabilities
                for capability, enabled in agent.capabilities.items():
                    if enabled:
                        await self._execute_capability(agent, capability)

                # Sleep for the configured interval
                await asyncio.sleep(agent.configuration.get("interval", 30))
        except asyncio.CancelledError:
            logger.info(f"Agent {agent.id} task cancelled")
        except Exception as e:
            logger.error(f"Error in agent {agent.id} task: {str(e)}")
            await self.stop_agent(agent.id)

    async def _execute_capability(self, agent: AgentModel, capability: str):
        """Execute a specific agent capability."""
        try:
            if capability == "monitoring":
                await self._execute_monitoring(agent)
            elif capability == "forensics":
                await self._execute_forensics(agent)
            elif capability == "response":
                await self._execute_response(agent)
            else:
                logger.warning(f"Unknown capability {capability} for agent {agent.id}")
        except Exception as e:
            logger.error(f"Error executing capability {capability} for agent {agent.id}: {str(e)}")

    async def _execute_monitoring(self, agent: AgentModel):
        """Execute monitoring capability."""
        # TODO: Implement monitoring logic
        pass

    async def _execute_forensics(self, agent: AgentModel):
        """Execute forensics capability."""
        # TODO: Implement forensics logic
        pass

    async def _execute_response(self, agent: AgentModel):
        """Execute response capability."""
        # TODO: Implement response logic
        pass

    async def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """Get the current status of an agent."""
        if agent_id not in self.active_agents:
            return None

        agent_data = self.active_agents[agent_id]
        return {
            "agent_id": agent_id,
            "status": "active",
            "started_at": agent_data["started_at"].isoformat(),
            "last_heartbeat": agent_data["last_heartbeat"].isoformat(),
            "capabilities": agent_data["agent"].capabilities
        }

    async def get_all_agent_statuses(self) -> List[Dict]:
        """Get the status of all active agents."""
        return [
            await self.get_agent_status(agent_id)
            for agent_id in self.active_agents
        ]

    async def cleanup(self):
        """Clean up all agents and resources."""
        try:
            # Stop all active agents
            for agent_id in list(self.active_agents.keys()):
                await self.stop_agent(agent_id)

            self._initialized = False
            logger.info("Agent manager cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during agent manager cleanup: {str(e)}")
    
    async def execute_task(self, task: Dict) -> Dict:
        """Execute a task using appropriate agents."""
        try:
            task_type = task.get("type")
            agent_type = task.get("agent_type")
            
            if agent_type not in self.agent_types:
                raise ValueError(f"Unknown agent type: {agent_type}")
            
            # Find appropriate agent
            agent = next(
                (a for a in self.agents.values() if isinstance(a, self.agent_types[agent_type])),
                None
            )
            
            if not agent:
                raise ValueError(f"No {agent_type} agent available")
            
            # Execute task
            result = await agent.execute(task)
            
            # Log execution
            self.logger.info(f"Executed {task_type} task using {agent_type} agent")
            
            return {
                "status": "success",
                "task_type": task_type,
                "agent_type": agent_type,
                "timestamp": datetime.utcnow().isoformat(),
                "result": result
            }
        except Exception as e:
            self.logger.error(f"Error executing task: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def coordinate_response(self, incident: Dict) -> Dict:
        """Coordinate a response to an incident using multiple agents."""
        try:
            # 1. Guardian Agent: Assess threat
            threat_assessment = await self.execute_task({
                "type": "threat_assessment",
                "agent_type": "guardian",
                "incident_data": incident
            })
            
            # 2. Simulation Agent: Model attack path
            attack_model = await self.execute_task({
                "type": "model_attack_path",
                "agent_type": "simulation",
                "threat_data": threat_assessment
            })
            
            # 3. Containment Agent: Implement containment
            containment = await self.execute_task({
                "type": "contain_threat",
                "agent_type": "containment",
                "threat_data": threat_assessment,
                "attack_model": attack_model
            })
            
            # 4. Forensic Agent: Collect evidence
            evidence = await self.execute_task({
                "type": "collect_evidence",
                "agent_type": "forensic",
                "incident_data": incident,
                "containment_data": containment
            })
            
            # 5. Compliance Agent: Handle documentation
            documentation = await self.execute_task({
                "type": "prepare_documentation",
                "agent_type": "compliance",
                "incident_data": incident,
                "evidence_data": evidence
            })
            
            return {
                "status": "coordinated",
                "timestamp": datetime.utcnow().isoformat(),
                "threat_assessment": threat_assessment,
                "attack_model": attack_model,
                "containment": containment,
                "evidence": evidence,
                "documentation": documentation
            }
        except Exception as e:
            self.logger.error(f"Error coordinating response: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            } 