import asyncio
import sys
import uuid
from datetime import datetime, timedelta, timezone

# Ensure app folder is in path
sys.path.insert(0, ".")

from app.db.session import AsyncSessionLocal
from app.models import User, Project, Audit, AuditMetrics, SEOOptimization

async def seed_rich_data():
    print("Beginning rich database seeding...")
    
    user_id = uuid.UUID("a12c3b4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d")
    
    projects_data = [
        {
            "id": uuid.UUID("f87a8b3e-e24c-4c60-84e9-270830db9df2"),
            "url": "https://newstigo.com",
            "scores": [62, 68, 78, 85, 94],
            "recommendations": [
                {
                    "path": "/gaming-news/starfield-review",
                    "original_title": "Starfield Game Review",
                    "original_desc": "Read our review of starfield game.",
                    "optimized_title": "Starfield Review: An Epic Sci-Fi Space Adventure",
                    "optimized_desc": "Starfield delivers an ambitious cosmic sandbox. Read our deep-dive review on gameplay, performance, and features inside."
                },
                {
                    "path": "/tech/cpu-benchmarks-2026",
                    "original_title": "New CPU Benchmarks 2026",
                    "original_desc": "Benchmarks for new CPUs.",
                    "optimized_title": "Top CPU Benchmarks 2026: Intel vs AMD Performance",
                    "optimized_desc": "Compare the fastest CPUs of 2026. Explore detailed synthetic benchmarks, thermal testing, and gaming performance results."
                }
            ]
        },
        {
            "id": uuid.UUID("3b2d6a5d-4f7b-40fa-ba41-d8a4f6b216c8"),
            "url": "https://techblogpro.io",
            "scores": [70, 75, 82, 88],
            "recommendations": [
                {
                    "path": "/seo/seo-guide-2026",
                    "original_title": "SEO Guide",
                    "original_desc": "Guide on how to improve your rankings.",
                    "optimized_title": "The Ultimate SEO Guide 2026: Rank Higher on Google",
                    "optimized_desc": "Master search engine optimization with our updated 2026 handbook. Step-by-step techniques to audit metadata and speed up sites."
                }
            ]
        },
        {
            "id": uuid.UUID("8a8b2c4d-612a-4b7b-891a-f12a3d4e5f6a"),
            "url": "https://myshophub.com",
            "scores": [55, 60, 64, 72],
            "recommendations": [
                {
                    "path": "/shop/wireless-headphones",
                    "original_title": "Buy Headphones",
                    "original_desc": "Headphones for sale.",
                    "optimized_title": "Buy Premium Wireless Noise-Cancelling Headphones",
                    "optimized_desc": "Get crystal clear sound and active noise cancellation. Order today for free express shipping and 1-year warranty."
                }
            ]
        },
        {
            "id": uuid.UUID("9c8d7e6f-5a4b-3c2d-1e0f-9a8b7c6d5e4f"),
            "url": "https://aerotech.io",
            "scores": [88, 92, 98, 100],
            "recommendations": [
                {
                    "path": "/features/speed-auditing",
                    "original_title": "AeroTech Speed Tool",
                    "original_desc": "Our tool scans pages quickly.",
                    "optimized_title": "AeroTech Core Web Vitals Tool: Auditing at Warp Speed",
                    "optimized_desc": "Diagnose LCP and layout shifts in milliseconds. Generate dynamic JSON-LD metadata schemas automatically."
                }
            ]
        }
    ]
    
    async with AsyncSessionLocal() as session:
        # Create user
        existing_user = await session.get(User, user_id)
        if not existing_user:
            user = User(
                id=user_id,
                email="test@aerotech.io",
                password_hash="pbkdf2_sha256$hashedpasswordval"
            )
            session.add(user)
            await session.flush()
            print("- User test@aerotech.io created.")
        
        # Create projects and audits
        for pdata in projects_data:
            existing_project = await session.get(Project, pdata["id"])
            if not existing_project:
                project = Project(
                    id=pdata["id"],
                    user_id=user_id,
                    domain_url=pdata["url"],
                    status="active"
                )
                session.add(project)
                await session.flush()
                print(f"- Project {pdata['url']} registered.")
            else:
                project = existing_project
                
            # Create historical audits
            score_count = len(pdata["scores"])
            for idx, score in enumerate(pdata["scores"]):
                # Calculate dates backwards
                audit_date = datetime.now(timezone.utc) - timedelta(days=(score_count - 1 - idx) * 5)
                
                # Check if audit at this specific score/date range exists
                audit = Audit(
                    id=uuid.uuid4(),
                    project_id=project.id,
                    overall_score=score,
                    created_at=audit_date
                )
                session.add(audit)
                await session.flush()
                
                # Create corresponding metrics
                metrics = AuditMetrics(
                    id=uuid.uuid4(),
                    audit_id=audit.id,
                    lcp=float(max(1.0, 4.5 - (idx * 0.7))),
                    cls=float(max(0.01, 0.25 - (idx * 0.05))),
                    mobile_score=int(score - 5),
                    desktop_score=int(min(100, score + 4)),
                    json_report={},
                )
                session.add(metrics)
                
                # If it's the latest audit, generate optimization recommendations
                if idx == score_count - 1:
                    for rec in pdata["recommendations"]:
                        opt = SEOOptimization(
                            id=uuid.uuid4(),
                            audit_id=audit.id,
                            url_path=rec["path"],
                            original_title=rec["original_title"],
                            original_description=rec["original_desc"],
                            optimized_title=rec["optimized_title"],
                            optimized_description=rec["optimized_desc"],
                            json_ld_schema={
                                "@context": "https://schema.org",
                                "@type": "Article",
                                "name": rec["optimized_title"],
                                "url": f"{pdata['url']}{rec['path']}",
                                "description": rec["optimized_desc"]
                            },
                            ai_status="pending",
                            created_at=audit_date
                        )
                        session.add(opt)
                        
            print(f"  * Generated {score_count} historical audits for {pdata['url']}.")
        
        await session.commit()
    print("Database rich seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_rich_data())
