from urllib.parse import urlparse
from app.db.session import AsyncSessionLocal
from app.models import SEOOptimization
from app.services.optimization.metadata_optimizer import MetadataOptimizer
from app.services.optimization.schema_optimizer import SchemaOptimizer

class OptimizationOrchestrator:
    """
    Orchestrates the execution of all optimization strategies (metadata, JSON-LD, etc.)
    and persists findings in the database.
    """

    def __init__(self):
        self.strategies = [
            MetadataOptimizer(),
            SchemaOptimizer()
        ]

    async def run_optimization_pipeline(self, audit_id, url: str, context: dict) -> dict:
        """
        Runs all configured strategies and commits results to the seo_optimizations table.
        """
        # Build shared context
        shared_context = {
            "title": context.get("title", ""),
            "description": context.get("description", ""),
            "headings": context.get("headings", {}),
            "url": url
        }

        # Execute strategies and aggregate results
        results = {}
        for strategy in self.strategies:
            res = await strategy.optimize(shared_context)
            results.update(res)

        # Parse URL path for database record
        try:
            parsed = urlparse(url)
            url_path = parsed.path if parsed.path else "/"
            if parsed.query:
                url_path += f"?{parsed.query}"
        except Exception:
            url_path = url

        # Persist to database
        async with AsyncSessionLocal() as session:
            db_opt = SEOOptimization(
                audit_id=audit_id,
                url_path=url_path,
                original_title=shared_context["title"],
                optimized_title=results.get("optimized_title"),
                original_description=shared_context["description"],
                optimized_description=results.get("optimized_description"),
                json_ld_schema=results.get("json_ld_schema"),
                ai_status="pending"
            )
            session.add(db_opt)
            await session.commit()

        return results
