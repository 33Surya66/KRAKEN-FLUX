from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ....models.database import Agent as AgentModel
from ....schemas import Agent, AgentCreate
from ....core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[Agent])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all agents."""
    agents = db.query(AgentModel).offset(skip).limit(limit).all()
    return agents

@router.get("/{agent_id}", response_model=Agent)
async def get_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific agent by ID."""
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("/", response_model=Agent)
async def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db)
):
    """Create a new agent."""
    db_agent = AgentModel(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.put("/{agent_id}", response_model=Agent)
async def update_agent(
    agent_id: int,
    agent: AgentCreate,
    db: Session = Depends(get_db)
):
    """Update an existing agent."""
    db_agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    for key, value in agent.dict().items():
        setattr(db_agent, key, value)
    
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    """Delete an agent."""
    db_agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(db_agent)
    db.commit()
    return {"message": "Agent deleted successfully"} 