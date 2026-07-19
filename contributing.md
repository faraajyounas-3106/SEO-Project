# CONTRIBUTING.MD: AeroTech SEO Suite Developer Guide

## 1. Prerequisites
Before beginning development, ensure the following tools are installed on your machine:
*   **Docker & Docker Compose**: Required for containerized orchestration of the services[cite: 1].
*   **Python 3.12+**: Required for the FastAPI backend and Celery workers[cite: 1].
*   **Node.js 20+ (LTS)**: Required for the Next.js frontend development environment[cite: 1].
*   **Git**: Version control management[cite: 1].

## 2. Step-by-Step Setup
1.  **Clone the Repository**: `git clone <repository-url>`[cite: 1].
2.  **Environment Setup**: Create a `.env` file in the root directory based on `.env.example`. Ensure you populate `DATABASE_URL`, `REDIS_URL`, and `GOOGLE_API_KEYS`[cite: 1].
3.  **Spin Up Infrastructure**: Execute `docker compose up --build` to initialize the PostgreSQL database, Redis cache, backend API, and frontend services[cite: 1].
4.  **Backend Dependencies**: If working directly on the backend, run `pip install -r backend/requirements.txt` within your virtual environment[cite: 1].
5.  **Frontend Dependencies**: Run `npm install` inside the `/frontend` directory[cite: 1].

## 3. Workflow & Conventions
*   **Branch Naming**: Use `feature/`, `fix/`, or `docs/` prefixes followed by a descriptive name (e.g., `feature/audit-engine-refactor`)[cite: 1].
*   **Commit Messages**: Follow the Conventional Commits specification (e.g., `feat: add AI optimization service`, `fix: resolve SSRF vulnerability`)[cite: 1].
*   **Code Style**:
    *   **Python**: Must adhere to PEP 8 standards and utilize `black` for auto-formatting[cite: 1].
    *   **TypeScript**: Follow the standard ESLint configuration provided in the repository[cite: 1].

## 4. Testing
*   **Backend Testing**: Run `pytest` from the root directory to execute the suite of unit and integration tests[cite: 1].
*   **Frontend Testing**: Run `npm test` to verify component health and UI logic[cite: 1].
*   **Pre-Commit Hooks**: Ensure all tests pass before submitting a Pull Request[cite: 1].