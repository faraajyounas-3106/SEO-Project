# Architecture.md: AeroTech SEO Suite

## 1. App Flow and High-Level Architecture
The system operates on an asynchronous event-driven architecture to ensure high performance and responsiveness.

*   **Request Lifecycle**:
    1.  **Frontend Entry**: The user interacts with the Next.js dashboard to trigger an audit for a specific domain.
    2.  **API Gateway**: The request is sent to the FastAPI backend, which validates the session, checks usage quotas via middleware, and creates an entry in `audit_tasks`.
    3.  **Background Processing**: The task is pushed to a Redis queue. A Celery worker picks up the job, performs web scraping, calls Google APIs, and executes the AI optimization engines.
    4.  **Data Persistence**: The worker writes raw metrics to `audit_metrics` (JSONB) and logs specific optimizations in `seo_optimizations`.
    5.  **State Synchronization**: The worker updates the `audit_tasks` status to 'completed'. The frontend, through real-time polling or WebSocket updates, detects the completion and refreshes the view.

## 2. Tech Stack
*   **Frontend**:
    *   Framework: Next.js (App Router).
    *   Language: TypeScript.
    *   Styling/UI: Tailwind CSS + Shadcn UI.
    *   Visualization: Recharts/Chart.js.
*   **Backend**:
    *   Framework: FastAPI (Python)[cite: 1].
    *   Task Queue: Celery + Redis[cite: 1].
    *   Scraping: BeautifulSoup4 + HTTPX (or Playwright)[cite: 1].
    *   AI Integration: Google GenAI SDK[cite: 1].
*   **Data & Infrastructure**:
    *   Primary Database: PostgreSQL[cite: 1].
    *   Containerization: Docker + Docker Compose[cite: 1].

## 3. File and Folder Structure
The repository follows a clean, modular structure to ensure separation of concerns:

```text
/aerotech-seo-suite
├── /backend (FastAPI)
│   ├── /app
│   │   ├── /api (Routes/Controllers)
│   │   ├── /services (Business logic: AuditService, OptimizerService)
│   │   ├── /tasks (Celery worker definitions)
│   │   ├── /models (SQLAlchemy models)
│   │   └── /core (Middleware, Config, Security)
├── /frontend (Next.js)
│   ├── /app (Pages & Layouts)
│   ├── /components (Shadcn UI components)
│   ├── /hooks (API/State hooks)
│   └── /lib (API client/Utility functions)
├── /docker
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── /docs (Markdown documentation)
└── .env (Environment variables)