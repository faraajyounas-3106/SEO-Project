import uuid
from pydantic import BaseModel

class AuditCreateRequest(BaseModel):
    project_id: uuid.UUID
    url: str

class AuditStatusResponse(BaseModel):
    task_id: uuid.UUID
    status: str
    progress_percentage: int
    error_message: str | None = None

    class Config:
        from_attributes = True
