from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ....models.database import Evidence as EvidenceModel
from ....schemas import Evidence, EvidenceCreate
from ....core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=List[Evidence])
async def list_evidence(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all evidence entries."""
    evidence = db.query(EvidenceModel).offset(skip).limit(limit).all()
    return evidence

@router.get("/{evidence_id}", response_model=Evidence)
async def get_evidence(
    evidence_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific evidence entry by ID."""
    evidence = db.query(EvidenceModel).filter(EvidenceModel.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence

@router.post("/", response_model=Evidence)
async def create_evidence(
    evidence: EvidenceCreate,
    db: Session = Depends(get_db)
):
    """Create a new evidence entry."""
    db_evidence = EvidenceModel(**evidence.dict())
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence

@router.put("/{evidence_id}", response_model=Evidence)
async def update_evidence(
    evidence_id: int,
    evidence: EvidenceCreate,
    db: Session = Depends(get_db)
):
    """Update an existing evidence entry."""
    db_evidence = db.query(EvidenceModel).filter(EvidenceModel.id == evidence_id).first()
    if not db_evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    
    for key, value in evidence.dict().items():
        setattr(db_evidence, key, value)
    
    db.commit()
    db.refresh(db_evidence)
    return db_evidence

@router.delete("/{evidence_id}")
async def delete_evidence(
    evidence_id: int,
    db: Session = Depends(get_db)
):
    """Delete an evidence entry."""
    db_evidence = db.query(EvidenceModel).filter(EvidenceModel.id == evidence_id).first()
    if not db_evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    
    db.delete(db_evidence)
    db.commit()
    return {"message": "Evidence deleted successfully"} 