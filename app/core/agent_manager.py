from typing import Dict, List, Optional, Type
import asyncio
import logging
from datetime import datetime

from ..agents.base_agent import BaseAgent
from ..agents.guardian_agent import GuardianAgent
from ..agents.forensic_agent import ForensicAgent
from ..agents.containment_agent import ContainmentAgent
from ..agents.compliance_agent import ComplianceAgent
from ..agents.simulation_agent import SimulationAgent

class AgentManager:
    """Manages and coordinates all KRAKEN-FLUX agents."""
    
    def __init__(self):
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
        """Initialize all agents in the system."""
        try:
            for agent_type, agent_class in self.agent_types.items():
                agent = agent_class()
                if await agent.initialize():
                    self.agents[agent.agent_id] = agent
                    self.logger.info(f"Initialized {agent_type} agent: {agent.agent_id}")
                else:
                    self.logger.error(f"Failed to initialize {agent_type} agent")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Error initializing agents: {str(e)}")
            return False
    
    async def cleanup(self) -> bool:
        """Clean up all agents in the system."""
        try:
            for agent_id, agent in self.agents.items():
                if await agent.cleanup():
                    self.logger.info(f"Cleaned up agent: {agent_id}")
                else:
                    self.logger.error(f"Failed to clean up agent: {agent_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error cleaning up agents: {str(e)}")
            return False
    
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
    
    async def get_agent_status(self) -> Dict:
        """Get status of all agents."""
        try:
            status = {}
            for agent_id, agent in self.agents.items():
                status[agent_id] = await agent.heartbeat()
            return status
        except Exception as e:
            self.logger.error(f"Error getting agent status: {str(e)}")
            return {}
    
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