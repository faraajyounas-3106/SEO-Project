import uuid
import logging
from fastapi import HTTPException, status, Depends
from sqlalchemy import select, func
from app.db.session import AsyncSessionLocal
from app.models import Audit, Project
from app.core.security import mask_sensitive_data

logger = logging.getLogger("audit_logger")

class UsageTracker:
    """
    Centralized service to track resource usage limits and record audit events.
    """
    
    # Config-driven limit (could be moved to Settings in config.py)
    MAX_AUDITS_PER_PROJECT = 5

    @classmethod
    async def check_quota(cls, project_id: uuid.UUID) -> bool:
        """
        Checks if the project has remaining audit quota.
        """
        async with AsyncSessionLocal() as session:
            stmt = select(func.count(Audit.id)).where(Audit.project_id == project_id)
            result = await session.execute(stmt)
            count = result.scalar() or 0
            return count < cls.MAX_AUDITS_PER_PROJECT

    @classmethod
    async def log_action(cls, user_id: uuid.UUID, action_type: str):
        """
        Audit Logging: Logs security-sensitive events with mask formatting.
        """
        raw_msg = f"SECURITY AUDIT: User={user_id} Action={action_type}"
        masked_msg = mask_sensitive_data(raw_msg)
        logger.info(masked_msg)

async def require_active_license(project_id: uuid.UUID):
    """
    FastAPI Dependency: Checks if the target project is under quota before running audits.
    """
    quota_available = await UsageTracker.check_quota(project_id)
    if not quota_available:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded: Quota for this project has been reached. Please upgrade your license plan."
        )
    return True
