import uuid
from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models import Project, Audit, User, SEOOptimization
from app.schemas.project import ProjectCreate, ProjectResponse
from urllib.parse import urlparse

router = APIRouter(prefix="/projects", tags=["Projects"])

def get_domain_name(url: str) -> str:
    """Helper to parse a user-friendly name from a URL."""
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc or parsed.path
        # Clean www.
        if netloc.startswith("www."):
            netloc = netloc[4:]
        # Capitalize name
        parts = netloc.split(".")
        if len(parts) > 0:
            return parts[0].capitalize() + " Portal"
        return "New Project"
    except Exception:
        return "New Project"

@router.get("", response_model=List[ProjectResponse])
async def list_projects():
    """
    List all projects in the database along with their latest audit scores.
    """
    async with AsyncSessionLocal() as session:
        # Fetch all projects
        projects_stmt = select(Project).order_by(Project.created_at.desc())
        projects_res = await session.execute(projects_stmt)
        projects = projects_res.scalars().all()
        
        response_data = []
        for p in projects:
            # Query the latest completed audit for this project
            audit_stmt = (
                select(Audit)
                .where(Audit.project_id == p.id)
                .order_by(Audit.created_at.desc())
                .limit(1)
            )
            audit_res = await session.execute(audit_stmt)
            latest_audit = audit_res.scalar_one_or_none()
            
            score = latest_audit.overall_score if latest_audit else None
            date_str = latest_audit.created_at.strftime("%Y-%m-%d") if latest_audit else None
            
            response_data.append(
                ProjectResponse(
                    id=p.id,
                    name=get_domain_name(p.domain_url),
                    domain_url=p.domain_url,
                    status=p.status,
                    created_at=p.created_at,
                    latest_score=score,
                    latest_audit_date=date_str
                )
            )
        return response_data

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate):
    """
    Creates a new project domain registration.
    """
    async with AsyncSessionLocal() as session:
        # Find or create a default test user
        user_stmt = select(User).limit(1)
        user_res = await session.execute(user_stmt)
        user = user_res.scalar_one_or_none()
        
        if not user:
            # Create default test user
            user = User(
                id=uuid.UUID("a12c3b4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"),
                email="test@aerotech.io",
                password_hash="pbkdf2_sha256$hashedpasswordval"
            )
            session.add(user)
            await session.flush()
        
        # Check if project domain already registered
        exist_stmt = select(Project).where(Project.domain_url == payload.domain_url)
        exist_res = await session.execute(exist_stmt)
        existing_project = exist_res.scalar_one_or_none()
        if existing_project:
            return ProjectResponse(
                id=existing_project.id,
                name=get_domain_name(existing_project.domain_url),
                domain_url=existing_project.domain_url,
                status=existing_project.status,
                created_at=existing_project.created_at
            )

        new_project = Project(
            id=uuid.uuid4(),
            user_id=user.id,
            domain_url=payload.domain_url,
            status="active"
        )
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)
        
        return ProjectResponse(
            id=new_project.id,
            name=get_domain_name(new_project.domain_url),
            domain_url=new_project.domain_url,
            status=new_project.status,
            created_at=new_project.created_at
        )

@router.get("/{project_id}/audits")
async def list_project_audits(project_id: uuid.UUID):
    """
    Returns historical list of audit scores for a specific project.
    """
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Audit)
            .where(Audit.project_id == project_id)
            .order_by(Audit.created_at.asc())
        )
        res = await session.execute(stmt)
        audits = res.scalars().all()
        return [
            {
                "id": str(a.id),
                "name": a.created_at.strftime("%b %d"),
                "Score": a.overall_score,
                "created_at": a.created_at.isoformat()
            }
            for a in audits
        ]

@router.get("/{project_id}/optimizations")
async def list_project_optimizations(project_id: uuid.UUID):
    """
    Returns latest AI optimizations generated for the target project.
    """
    async with AsyncSessionLocal() as session:
        # Find latest audit
        audit_stmt = (
            select(Audit)
            .where(Audit.project_id == project_id)
            .order_by(Audit.created_at.desc())
            .limit(1)
        )
        audit_res = await session.execute(audit_stmt)
        latest_audit = audit_res.scalar_one_or_none()
        
        if not latest_audit:
            return []
            
        opt_stmt = (
            select(SEOOptimization)
            .where(SEOOptimization.audit_id == latest_audit.id)
            .order_by(SEOOptimization.created_at.desc())
        )
        opt_res = await session.execute(opt_stmt)
        opts = opt_res.scalars().all()
        
        return [
            {
                "id": str(opt.id),
                "path": opt.url_path,
                "type": "Metadata",
                "original": {
                    "title": opt.original_title or "Missing Title",
                    "desc": opt.original_description or "Missing Description"
                },
                "optimized": {
                    "title": opt.optimized_title or "Optimized Title",
                    "desc": opt.optimized_description or "Optimized Description"
                },
                "status": opt.ai_status
            }
            for opt in opts
        ]
