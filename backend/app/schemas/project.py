import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str = Field(..., description="User-friendly name of the project")
    domain_url: str = Field(..., description="Target website URL to run audits against")

class ProjectResponse(BaseModel):
    id: uuid.UUID
    name: Optional[str] = None
    domain_url: str
    status: str
    created_at: datetime
    latest_score: Optional[int] = None
    latest_audit_date: Optional[str] = None

    class Config:
        from_attributes = True
