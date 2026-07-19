Phase 1 Checklist (The "Hard" Goals)
[ ] Git repository initialized with .gitignore.

[ ] Standardized folder structure created.

[ ] docker-compose.yml operational, orchestrating 5 services (db, cache, api, worker, web).

[ ] Backend (FastAPI) connected to Database (PostgreSQL).

[ ] Database Migrations (Alembic) initialized.

[ ] Frontend (Next.js) running with Tailwind/Shadcn and successfully pinging the Backend health check.

Step-by-Step Execution Plan
Step 1: Repository Initialization & Structure
Action: Create the root project folder (aerotech-seo-suite).

Action: Initialize Git (git init).

Action: Create a strict .gitignore (to exclude node_modules, __pycache__, .env, and build files).

Action: Create the top-level directories: /backend, /frontend, /docker.

Step 2: Docker & Infrastructure Configuration
Goal: Define how the five services talk to each other in isolation.

Action: Create /docker/Dockerfile.backend (multi-stage build for FastAPI/Celery).

Action: Create /docker/Dockerfile.frontend (multi-stage build for Next.js).

Action: Create root docker-compose.yml.

Defines db (Postgres) with persistent volume.

Defines cache (Redis).

Defines api (FastAPI) using Dockerfile.backend.

Defines worker (Celery) using the same image as api.

Defines web (Next.js) using Dockerfile.frontend.

Sets up Docker internal networking so services refer to each other by hostname (e.g., db, redis).

Step 3: Backend Initialization
Goal: Get FastAPI running and talking to Postgres.

Action: Create backend/requirements.txt (FastAPI, SQLAlchemy, Alembic, asyncpg, pydantic-settings).

Action: Initialize the FastAPI app structure inside backend/app/.

Action: Create backend/app/core/config.py (to load DATABASE_URL from env).

Action: Create backend/app/db/session.py (SQLAlchemy engine setup).

Action: Create backend/app/main.py (root app with a /health endpoint).

Action: Run Alembic init (alembic init alembic) inside the backend container to manage schema.

Step 4: Frontend Initialization
Goal: Get Next.js running with Tailwind and connecting to the API.

Action: Run npx create-next-app@latest frontend (TypeScript, Tailwind, App Router).

Action: Initialize Shadcn UI in the frontend project.

Action: Create frontend/lib/api.ts (a configured fetch client pointing to the Docker backend internal URL).

Action: Modify the default frontend/app/page.tsx to become a simple "Hello World" dashboard.

Action: Add a useEffect hook to this page that calls the Backend /health endpoint on load and displays "API Connected" or "API Disconnected".

Step 5: Verification & Commit
Goal: Verify the "Working Extent" of Phase 1.

Action: Run docker compose up --build.

Action: Open browser to http://localhost:3000 (Frontend).

Verify: The UI loads, shows the "Hello World" message, and the status indicator confirms "API Connected".

Action: If successful, stop containers and execute git commit -m "feat: Phase 1 infrastructure and hello world".