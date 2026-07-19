# API.md: AeroTech SEO Suite Endpoint Specification

## 1. Audit Management Endpoints

### POST /api/v1/audits
*   **Purpose**: Trigger a new website audit process[cite: 1].
*   **Payload (JSON)**: 
    ```json
    {
      "project_id": "UUID",
      "url": "[https://example.com](https://example.com)"
    }
    ```
*   **Response (202 Accepted)**:
    ```json
    {
      "task_id": "UUID",
      "status": "queued",
      "message": "Audit request received and queued for processing"
    }
    ```

### GET /api/v1/audits/{task_id}/status
*   **Purpose**: Poll the status of an ongoing or completed audit[cite: 1].
*   **Response (200 OK)**:
    ```json
    {
      "task_id": "UUID",
      "status": "processing",
      "progress_percentage": 45
    }
    ```

## 2. Error Code Definitions
*   **429 Too Many Requests**: Returned when the API limit for a user tier is exceeded or the target site has rate-limited the scraper[cite: 1].
    *   *Body*: `{ "error_code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests. Please try again in X minutes." }`[cite: 1].
*   **400 Bad Request**: Returned if the provided URL fails validation or is deemed an internal/malicious network address[cite: 1].
*   **401 Unauthorized**: Returned if the session token is missing or expired[cite: 1].
*   **500 Internal Server Error**: Returned if the AI processing pipeline or scraping engine encounters an unhandled exception[cite: 1].

## 3. Authentication Requirements
*   **Header Requirement**: All API endpoints (except login/register) require an `Authorization: Bearer <JWT_TOKEN>` header[cite: 1].
*   **Session Validation**: Every request is validated against the active database session; if a user's license is inactive, the `UsageTracker` middleware will reject the request with a `403 Forbidden` status[cite: 1].