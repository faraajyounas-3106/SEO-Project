import asyncio
import sys
# Ensure app folder is in path
sys.path.insert(0, ".")

from app.db.session import engine
from app.models import Base

async def init_models():
    print("Connecting to database and creating tables...")
    async with engine.begin() as conn:
        # Creates all tables (users, projects, audits, audit_metrics, seo_optimizations, audit_tasks)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
