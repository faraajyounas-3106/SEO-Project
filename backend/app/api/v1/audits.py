import uuid
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import AuditTask, Project
from app.schemas.audit import AuditCreateRequest, AuditStatusResponse
from app.core.security import is_safe_url, sanitize_url
from app.core.usage import require_active_license
from app.worker import run_page_audit

router = APIRouter(prefix="/audits", tags=["Audits"])

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def create_audit_task(payload: AuditCreateRequest):
    """
    Triggers a new website audit by creating an AuditTask and queueing a Celery job.
    """
    # 0. Quota check & licensing verification
    await require_active_license(payload.project_id)
    
    # 1. Sanitize the URL before processing
    payload.url = sanitize_url(payload.url)
    # 1. SSRF Protection: Reject unsafe or local target URLs
    if not is_safe_url(payload.url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The URL provided is invalid or points to an unsafe internal/reserved network range."
        )

    async with AsyncSessionLocal() as session:
        # Verify the project exists
        project_stmt = select(Project).where(Project.id == payload.project_id)
        project_res = await session.execute(project_stmt)
        project = project_res.scalar_one_or_none()
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project with the specified ID does not exist."
            )

        # Create task entry
        task = AuditTask(
            project_id=payload.project_id,
            status="queued",
            progress_percentage=0
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

    # 2. Trigger asynchronous background Celery worker
    run_page_audit.delay(str(task.id), payload.url)

    return {
        "task_id": task.id,
        "status": "queued",
        "message": "Audit request received and queued for processing"
    }

@router.get("/{task_id}/status", response_model=AuditStatusResponse)
async def get_audit_status(task_id: uuid.UUID):
    """
    Retrieves the execution status and progress of an ongoing or completed audit task.
    """
    async with AsyncSessionLocal() as session:
        stmt = select(AuditTask).where(AuditTask.id == task_id)
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audit task with the specified ID does not exist."
            )

        return task
