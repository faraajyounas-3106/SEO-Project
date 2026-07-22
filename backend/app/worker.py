import asyncio
from celery import Celery
from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models import AuditTask, Audit, AuditMetrics
from app.services.audit import AuditService
from app.services.pagespeed import PageSpeedService
from sqlalchemy import update, select

# Initialize Celery Application
celery_app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_transport_options={"protocol": 2},
    redis_backend_transport_options={"protocol": 2},
)

from app.services.optimization.orchestrator import OptimizationOrchestrator

async def _run_audit_async(task_id_str: str, url: str):
    import uuid
    task_id = uuid.UUID(task_id_str)
    
    # 1. Update task to processing and set progress
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(AuditTask)
            .where(AuditTask.id == task_id)
            .values(status="processing", progress_percentage=20)
        )
        await session.commit()
        
    try:
        # 2. Update task progress to scraping stage
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(AuditTask)
                .where(AuditTask.id == task_id)
                .values(progress_percentage=40)
            )
            await session.commit()
            
        html_content = await AuditService.scrape_page(url)
        dom_metrics = AuditService.parse_dom(html_content, url)
        
        # 3. Update task progress to PageSpeed analysis stage
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(AuditTask)
                .where(AuditTask.id == task_id)
                .values(progress_percentage=70)
            )
            await session.commit()
            
        ps_metrics = await PageSpeedService.fetch_all_metrics(url)
        
        # 4. Save results to Database
        combined_report = {
            "seo_elements": dom_metrics,
            "mobile_pagespeed": ps_metrics["mobile"]["raw_report"],
            "desktop_pagespeed": ps_metrics["desktop"]["raw_report"]
        }
        
        async with AsyncSessionLocal() as session:
            # Query project_id corresponding to this task
            stmt = select(AuditTask.project_id).where(AuditTask.id == task_id)
            result = await session.execute(stmt)
            project_id = result.scalar_one()
            
            # Create persistent Audit log
            overall_score = int((ps_metrics["mobile"]["score"] + ps_metrics["desktop"]["score"]) / 2)
            db_audit = Audit(
                project_id=project_id,
                overall_score=overall_score
            )
            session.add(db_audit)
            await session.flush()  # Populates db_audit.id
            
            # Save metrics parameters (LCP, CLS, etc.)
            db_metrics = AuditMetrics(
                audit_id=db_audit.id,
                lcp=max(ps_metrics["mobile"]["lcp"], ps_metrics["desktop"]["lcp"]),
                cls=max(ps_metrics["mobile"]["cls"], ps_metrics["desktop"]["cls"]),
                mobile_score=ps_metrics["mobile"]["score"],
                desktop_score=ps_metrics["desktop"]["score"],
                json_report=combined_report
            )
            session.add(db_metrics)
            
            # Commit the Audit and Metrics first so the Foreign Key constraints are satisfied
            await session.commit()
            
        # 5. Run AI Optimization Pipeline (after committing the parent audit)
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(AuditTask)
                .where(AuditTask.id == task_id)
                .values(progress_percentage=90)
            )
            await session.commit()
            
        orchestrator = OptimizationOrchestrator()
        await orchestrator.run_optimization_pipeline(db_audit.id, url, dom_metrics)
        
        # Mark task as completed (progress 100)
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(AuditTask)
                .where(AuditTask.id == task_id)
                .values(status="completed", progress_percentage=100)
            )
            await session.commit()
            
    except Exception as e:
        # Fallback database connection session to store failure state
        async with AsyncSessionLocal() as session:
            await session.execute(
                update(AuditTask)
                .where(AuditTask.id == task_id)
                .values(status="failed", error_message=str(e), progress_percentage=100)
            )
            await session.commit()
        raise e

@celery_app.task(name="app.worker.run_page_audit")
def run_page_audit(task_id_str: str, url: str):
    """
    Synchronous Celery task wrapper calling the async handler.
    """
    asyncio.run(_run_audit_async(task_id_str, url))
