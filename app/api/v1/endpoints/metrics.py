from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ....models.database import SystemMetrics as SystemMetricsModel
from ....schemas import SystemMetrics, SystemMetricsCreate
from ....core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[SystemMetrics])
async def list_metrics(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all system metrics entries."""
    metrics = db.query(SystemMetricsModel).offset(skip).limit(limit).all()
    return metrics

@router.get("/{metric_id}", response_model=SystemMetrics)
async def get_metric(
    metric_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific system metric entry by ID."""
    metric = db.query(SystemMetricsModel).filter(SystemMetricsModel.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="System metric not found")
    return metric

@router.post("/", response_model=SystemMetrics)
async def create_metric(
    metric: SystemMetricsCreate,
    db: Session = Depends(get_db)
):
    """Create a new system metric entry."""
    db_metric = SystemMetricsModel(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.put("/{metric_id}", response_model=SystemMetrics)
async def update_metric(
    metric_id: int,
    metric: SystemMetricsCreate,
    db: Session = Depends(get_db)
):
    """Update an existing system metric entry."""
    db_metric = db.query(SystemMetricsModel).filter(SystemMetricsModel.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="System metric not found")
    
    for key, value in metric.dict().items():
        setattr(db_metric, key, value)
    
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.delete("/{metric_id}")
async def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db)
):
    """Delete a system metric entry."""
    db_metric = db.query(SystemMetricsModel).filter(SystemMetricsModel.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="System metric not found")
    
    db.delete(db_metric)
    db.commit()
    return {"message": "System metric deleted successfully"} 