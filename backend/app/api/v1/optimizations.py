import uuid
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import SEOOptimization

router = APIRouter(prefix="/optimizations", tags=["Optimizations"])

class StatusUpdateRequest(BaseModel):
    status: str  # 'applied' or 'skipped'

@router.patch("/{opt_id}")
async def update_optimization_status(opt_id: uuid.UUID, payload: StatusUpdateRequest):
    """
    Update status of a recommendation to applied or skipped.
    """
    if payload.status not in ("applied", "skipped", "pending"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status value. Must be 'applied', 'skipped', or 'pending'."
        )
        
    async with AsyncSessionLocal() as session:
        opt_stmt = select(SEOOptimization).where(SEOOptimization.id == opt_id)
        res = await session.execute(opt_stmt)
        opt = res.scalar_one_or_none()
        
        if not opt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Optimization recommendation not found."
            )
            
        opt.ai_status = payload.status
        await session.commit()
        return {"id": str(opt.id), "status": opt.ai_status}
