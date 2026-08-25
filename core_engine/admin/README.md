# Admin Control Console & Site Management Subsystem

The `core_engine/admin` module provides administrative endpoints and management controls for the **CareerPulse** platform. It enables administrators to monitor system telemetry, publish global announcement banners, configure maintenance modes and feature flags, manage user accounts, and clear telemetry activity logs.

---

## 1. Technical Stack & Capabilities

- **Framework:** FastAPI APIRouter (`/api/v1/admin`)
- **Security & Authorization:** Bearer token validation with role enforcement (`role == "admin"`)
- **Telemetry Integration:** Interfaces directly with `TelemetryService` for hardware load (`psutil` CPU %, RAM MB/%, Uptime), platform usage counters, and audit logs
- **User Account Management:** Interfaces with `AuthService` for account queries and administrative deletion
- **Data Validation:** Pydantic schemas for administrative authentication and settings updates
- **Error Policy:** Explicit HTTP status codes (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`)

---

## 2. Key Capabilities & Endpoints

| Method | Endpoint | Description | Access Control | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/admin/login` | Authenticates administrator credentials and returns a 7-day JWT token | Public | `200`, `401`, `403` |
| `GET` | `/api/v1/admin/me` | Returns current authenticated administrator profile | Admin Token Required | `200`, `401`, `403` |
| `GET` | `/api/v1/admin/telemetry` | Retrieves system hardware stats (CPU, RAM, Uptime), activity metrics, and audit logs | Admin Token Required | `200`, `401`, `403` |
| `GET` | `/api/v1/admin/settings` | Returns active site configuration (announcement banner, maintenance mode, feature flags) | Public | `200` |
| `POST` | `/api/v1/admin/settings` | Updates site settings (banner text/visibility, maintenance toggle, feature flags) | Admin Token Required | `200`, `401`, `403` |
| `GET` | `/api/v1/admin/users` | Lists all registered candidate user accounts | Admin Token Required | `200`, `401`, `403` |
| `DELETE` | `/api/v1/admin/users/{user_id}` | Deletes a specified user account from persistent storage | Admin Token Required | `200`, `400`, `401`, `403`, `404` |
| `POST` | `/api/v1/admin/clear-logs` | Clears all recorded telemetry activity audit logs | Admin Token Required | `200`, `401`, `403` |

---

## 3. Directory Structure

```text
core_engine/admin/
├── README.md       # Subsystem documentation (this file)
├── router.py       # FastAPI routing, admin login, settings, users, and audit log endpoints
└── schemas.py      # Pydantic models for admin login and settings updates
```

---

## 4. Architectural Deep Dive

### `router.py`
- **`get_current_admin(authorization)`**: Dependency guard verifying the Bearer token and enforcing administrative privileges (`user.role == "admin"`). Raises HTTP `401` if token is missing/expired, and HTTP `403` if account lacks admin role.
- **`admin_login(data)`**: Validates administrative credentials against the user database and logs `ADMIN_LOGIN` telemetry events with admin ID metadata.
- **`get_telemetry_data()`**: Combines real-time `psutil` system metrics, platform counters, and user list into an administrative dashboard summary.
- **`get_site_settings()`**: Public endpoint allowing the frontend to retrieve global banner and feature flag status.
- **`update_site_settings(settings_data)`**: Updates global announcement banner, maintenance mode toggle, and feature flags (`enable_resume_upload`, `enable_jd_analyzer`, `enable_expert_calls`).
- **`list_registered_users()`**: Returns full list of registered candidate accounts.
- **`delete_user_account(user_id)`**: Deletes candidate accounts while preventing an administrator from deleting their own active session (`HTTP 400`).
- **`clear_telemetry_logs()`**: Clears audit event logs in `telemetry_db.json`.

### `schemas.py`
- **`AdminLogin`**: Pydantic schema validating admin login requests (`email`, `password`).
- **`SiteSettingsUpdate`**: Pydantic schema allowing partial updates:
  - `announcement_banner` (`Optional[str]`)
  - `announcement_active` (`Optional[bool]`)
  - `maintenance_mode` (`Optional[bool]`)
  - `enable_expert_calls` (`Optional[bool]`)
  - `enable_resume_upload` (`Optional[bool]`)
  - `enable_jd_analyzer` (`Optional[bool]`)

---

## 5. Security & Default Credentials

- **Default Administrator Account:** Seeded automatically on startup in `users_db.json`:
  - **Email:** `admin@careerpulse.ai`
  - **Password:** `admin123`
  - **Role:** `admin`
- All sensitive management operations enforce standard HTTP `401 Unauthorized` (missing/invalid token) and `403 Forbidden` (non-admin role) status codes.
