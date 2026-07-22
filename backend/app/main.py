from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.session import AsyncSessionLocal
from app.api.v1.audits import router as audits_router
from app.api.v1.projects import router as projects_router
from app.api.v1.optimizations import router as optimizations_router

app = FastAPI(title="AeroTech SEO Suite")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(audits_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(optimizations_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    db_status = "offline"
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        db_status = "online"
    except Exception as e:
        # In a real environment, you'd log this properly. We log to stderr/stdout.
        print(f"Database connection verification failed: {e}")

    if db_status == "online":
        return {"status": "online", "message": "API and Database Connected"}
    else:
        return {"status": "error", "message": "API Connected, Database Offline"}