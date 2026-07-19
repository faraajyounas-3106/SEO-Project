Things left:

1. Action: Create root docker-compose.yml.

Defines db (Postgres) with persistent volume.

Defines cache (Redis).

Defines api (FastAPI) using Dockerfile.backend.

Defines worker (Celery) using the same image as api.

Defines web (Next.js) using Dockerfile.frontend.

Sets up Docker internal networking so services refer to each other by hostname (e.g., db, redis).


2.Run Alembic init (alembic init alembic) inside the backend container to manage schema.

3.Create a strict .gitignore (to exclude node_modules, __pycache__, .env, and build files).

4.Action: Add a useEffect hook to this page that calls the Backend /health endpoint on load and displays "API Connected" or "API Disconnected".

5.