# Phases.md: AeroTech SEO Suite Development Roadmap

This project follows an incremental delivery model. Each phase culminates in a deployable, functional increment of the application, ensuring the system remains in a working state throughout the development lifecycle.

## Phase 1: Infrastructure & "Hello World" (Days 1-5)
* **Goal**: Full stack containerization and inter-service connectivity.
* **Deliverables**:
    * Configure `docker-compose.yml` to orchestrate PostgreSQL, Redis, FastAPI (API), and Next.js (Web)[cite: 1].
    * Initialize the database schema (Tables: `users`, `projects`, `audit_tasks`) using Alembic for migrations[cite: 1].
    * Set up the Next.js framework with Shadcn UI and Tailwind CSS, implementing a "Hello World" dashboard that successfully queries the FastAPI status endpoint[cite: 1].
* **Deadline**: 5 Days from Start.

## Phase 2: Core Audit Engine & Scraping (Days 6-12)
* **Goal**: Enable raw data acquisition from target domains.
* **Deliverables**:
    * Implement `AuditService` using `HTTPX` and `BeautifulSoup4` for robust DOM parsing[cite: 1].
    * Develop the Google PageSpeed Insights API integration layer to fetch Core Web Vitals (LCP, CLS, FID)[cite: 1].
    * Set up Celery/Redis workers to process audit tasks asynchronously; the dashboard must reflect the `audit_tasks` status changes[cite: 1].
* **Deadline**: 7 Days after Phase 1.

## Phase 3: AI Optimization Pipeline (Days 13-19)
* **Goal**: Integrate LLM intelligence for content and structural refinement.
* **Deliverables**:
    * Create the `OptimizerStrategy` pattern interface, allowing interchangeable logic for Image, Text, and Schema optimization[cite: 1].
    * Integrate Google GenAI SDK to generate SEO-focused meta-titles and descriptions based on raw site content[cite: 1].
    * Implement the automated JSON-LD schema markup injection engine[cite: 1].
* **Deadline**: 7 Days after Phase 2.

## Phase 4: SaaS Dashboard & Real-Time UX (Days 20-29)
* **Goal**: Build high-fidelity visualization and responsive control panels.
* **Deliverables**:
    * Implement Recharts/Chart.js for historical audit performance visualization[cite: 1].
    * Develop the "Audit Details" page with glassmorphic cards showing real-time `audit_metrics` and the "Apply/Ignore" optimization panel[cite: 1].
    * Add polling mechanisms to ensure the UI updates seamlessly as background workers progress[cite: 1].
* **Deadline**: 10 Days after Phase 3.

## Phase 5: Licensing, Metering & Security (Days 30-34)
* **Goal**: Production-grade guardrails and monetization readiness.
* **Deliverables**:
    * Implement `UsageTracker` service and `@require_active_license` decorators for feature gating[cite: 1].
    * Hardening: Add URL sanitization and SSRF prevention middleware to the crawler engine[cite: 1].
    * Audit logging: Implement PII/token masking for all system log outputs[cite: 1].
* **Deadline**: 5 Days after Phase 4.

## Phase 6: Testing & Deployment Readiness (Days 35-38)
* **Goal**: Final validation and system hardening.
* **Deliverables**:
    * Complete a full suite of integration tests (pytest for backend, Jest/Cypress for frontend)[cite: 1].
    * Finalize `CONTRIBUTING.md` and automated deployment scripts[cite: 1].
    * Database snapshotting and migration security verification[cite: 1].
* **Deadline**: 4 Days after Phase 5.