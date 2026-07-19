# Rules.md: AeroTech SEO Suite Development Guidelines

## 1. What to Use (Standards)
*   **Asynchronous Programming**: All backend I/O operations (API calls, database queries, web scraping) must be asynchronous using `async/await` to maintain high concurrency[cite: 1].
*   **Modular Architecture**: Follow the Controller-Service pattern; business logic must reside in `services/`, while routes in `api/` must only handle request validation and response formatting[cite: 1].
*   **Type Safety**: Use TypeScript for the frontend and Python Type Hints for the backend to ensure code maintainability and reduce runtime errors.
*   **Configuration**: All environment-specific settings (API keys, database URLs, optimization thresholds) must be stored in `.env` files or a centralized `config.py` file; hardcoding constants is strictly prohibited[cite: 1].

## 2. What to Avoid
*   **Tight Coupling**: Avoid direct dependencies between the frontend and the database. All interactions must go through the FastAPI backend API layer[cite: 1].
*   **Blocking Operations**: Never perform long-running tasks (e.g., heavy scraping or large AI generations) inside a request-response loop; these must be offloaded to Celery workers[cite: 1].
*   **Infrastructure Assumptions**: Do not assume the presence of global environment variables; always use a robust configuration loader (like `pydantic-settings` for Python) to validate configuration at startup.
*   **Unsafe Requests**: Never perform raw requests to user-provided URLs without sanitization and validation against internal network IP ranges to prevent SSRF[cite: 1].

## 3. Libraries and Error Handling
*   **Standardized Error Responses**: All API errors must return a consistent JSON structure: `{ "error_code": "...", "message": "...", "details": "..." }`.
*   **Library Preferences**: 
    *   Scraping: `BeautifulSoup4` with `HTTPX` for standard tasks; `Playwright` only for JS-heavy sites.
    *   Data: `SQLAlchemy` for ORM interactions.
    *   Background: `Celery` + `Redis` for distributed task management.
*   **Defensive Programming**: Every external API call (Google PageSpeed, etc.) must be wrapped in a `try-except` block with a timeout to handle network failures or API down-time gracefully[cite: 1].

## 4. Boundaries of AI
*   **No Autonomous Deployment**: The AI can generate, refactor, and explain code, but it shall not have direct access to deploy or modify production server infrastructure without explicit human review.
*   **Privacy Guardrails**: The AI must not store, log, or hardcode any actual user credentials, PII (Personally Identifiable Information), or production API keys in the generated documentation or `Memory.md` file[cite: 1].
*   **Logical Verification**: While the AI assists in architecture design, the developer (user) retains final responsibility for verifying that generated algorithms adhere to the "Strategy" and "Factory" design patterns defined in the project architecture[cite: 1].
*   **Hallucination Check**: If the AI suggests a library or a method that deviates from the approved tech stack in `Architecture.md`, it must be challenged and forced to align with the predefined project constraints[cite: 1].