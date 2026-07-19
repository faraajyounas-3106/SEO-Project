# security.md: AeroTech SEO Suite Security Standards

## 1. Secrets Management
*   **Zero Hardcoding Policy**: Under no circumstances shall API keys, database credentials, or secret tokens be hardcoded in the source code.
*   **Environment Variables**: All sensitive configuration must be managed via `.env` files (excluded from version control via `.gitignore`) and loaded at runtime using a secure configuration manager like `pydantic-settings`[cite: 1].
*   **Secrets Rotation**: API keys for external services (e.g., Google APIs) must be rotated periodically. If a secret is committed to a repository by accident, it must be considered compromised and rotated immediately[cite: 1].

## 2. URL Validation and Sanitization
*   **SSRF Prevention**: The backend must never perform requests to arbitrary user-provided URLs without first validating the domain against a whitelist or ensuring the IP address does not resolve to internal network ranges (e.g., `127.0.0.1`, `169.254.169.254`)[cite: 1].
*   **Sanitization**: All URL inputs must be sanitized to remove malicious query parameters or malformed characters before being passed to the `BeautifulSoup` or `HTTPX` request handlers[cite: 1].
*   **Protocol Restriction**: The crawler shall strictly enforce `http` and `https` protocols and reject non-web protocols (e.g., `file://`, `gopher://`)[cite: 1].

## 3. Logging Standards
*   **PII/Credential Masking**: Any function responsible for logging API requests or audit metadata must implement a masking utility to redact sensitive strings such as `Authorization` headers, session cookies, and user passwords[cite: 1].
*   **Log Redaction**: Masked strings should be logged as `[REDACTED]` or partial strings (e.g., `AIzaSy...****`) to ensure developers can debug without exposing production security tokens[cite: 1].
*   **Audit Logging**: Every security-sensitive action (e.g., login, password change, license modification) must be logged with a timestamp and user ID for forensic review[cite: 1].

## 4. Database Migrations
*   **Execution Policy**: Database migrations (using Alembic or equivalent) must never be run directly against a production database from a local development machine[cite: 1].
*   **Version Control**: Migration scripts must be peer-reviewed for security implications before being merged into the main branch[cite: 1].
*   **Backup Requirement**: A full database snapshot must be taken immediately before applying any schema migration to allow for instant rollback in the event of failure[cite: 1].