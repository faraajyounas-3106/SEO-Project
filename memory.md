# Memory.md: AeroTech SEO Suite Project State

## 1. Executive Summary
* **Project Status**: Planning Phase Complete.
* **Architecture Philosophy**: Incremental delivery (each phase results in a working system increment).
* **Git Strategy**: `main` (stable/production-ready), `feature/phase-x` (development). 

## 2. Technical Blueprint
* **Tech Stack**: 
    * Backend: FastAPI (Python), PostgreSQL, Redis, Celery.
    * Frontend: Next.js (TypeScript), Tailwind CSS, Shadcn UI, Recharts.
* **Design System**: Glassmorphism (Deep Navy base: #0B0E14, Neon Cyan: #00F2FF, Magenta: #FF007A).
* **Design Patterns**: Observer (Real-time UI), Strategy (Optimizers), Factory (Data Fetching), Controller/Service (Logic separation).

## 3. Directory Structure Snapshot
/aerotech-seo-suite
├── /backend
│   ├── /app (api, services, tasks, models, core)
├── /frontend
│   ├── /app, /components, /hooks, /lib
├── /docker
│   ├── Dockerfile.backend, Dockerfile.frontend, docker-compose.yml
├── /docs
│   ├── PRD.md, Architecture.md, Rules.md, Phases.md, Design.md, Security.md, API.md, Contributing.md
└── .env (Template)

## 4. Operational Guardrails
* **Secrets**: No hardcoding; use `pydantic-settings`.
* **Security**: SSRF protection active for all scrapers; logging redacts PII.
* **AI Boundaries**: No autonomous deployment; manual review required for production changes.

## 5. Development Progress
* **Current Milestone**: Initialization of Phase 1 (Infrastructure & Hello World).