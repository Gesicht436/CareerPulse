# Admin Control Console & Site Management Subsystem

The `core_engine/admin` module provides administrative endpoints and management controls for the **CareerPulse** platform. It enables administrators to monitor system telemetry, publish global announcement banners, configure maintenance modes and feature flags, manage user accounts, and clear telemetry activity logs.

---

## 1. Technical Stack & Capabilities

- **Framework:** FastAPI APIRouter (`/api/v1/admin`)
- **Security & Authorization:** Bearer token validation with role enforcement (`role == "admin"`)
- **Telemetry Integration:** Interfaces directly with `TelemetryService` for hardware load and platform usage metrics
- **User Account Management:** Interfaces with `AuthService` for account queries and administrative deletion
- **Data Validation:** Pydantic schemas for administrative authentication and settings updates

---

## 2. Key Capabilities & Endpoints

| Method | Endpoint | Description | Access Control |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/admin/login` | Authenticates administrator credentials and returns a 7-day JWT token | Public |
| `GET` | `/api/v1/admin/me` | Returns current authenticated administrator profile | Admin Token Required |
| `GET` | `/api/v1/admin/telemetry` | Retrieves system hardware stats (CPU, RAM, Uptime), activity metrics, and audit logs | Admin Token Required |
| `GET` | `/api/v1/admin/settings` | Returns active site configuration (announcement banner, maintenance mode, feature flags) | Public |
| `POST` | `/api/v1/admin/settings` | Updates site settings (banner text/visibility, maintenance toggle, feature flags) | Admin Token Required |
| `GET` | `/api/v1/admin/users` | Lists all registered candidate user accounts | Admin Token Required |
| `DELETE` | `/api/v1/admin/users/{user_id}` | Deletes a specified user account from persistent storage | Admin Token Required |
| `POST` | `/api/v1/admin/clear-logs` | Clears all recorded telemetry activity audit logs | Admin Token Required |

---

## 3. Directory Structure

```text
core_engine/admin/
├── README.md       # Subsystem documentation (this file)
├── router.py       # FastAPI routing and route-level authorization guards
└── schemas.py      # Pydantic models for admin login and settings updates
```

---

## 4. Key Components

### `router.py`
- **`get_current_admin(authorization)`**: Dependency guard verifying the Bearer token and enforcing administrative privileges (`user.role == "admin"`).
- **`admin_login(data)`**: Validates administrative credentials against the user database and logs `ADMIN_LOGIN` telemetry events.
- **`get_telemetry_data()`**: Combines real-time `psutil` system metrics, platform counters, and user list into an administrative dashboard summary.
- **`update_site_settings(settings_data)`**: Updates global announcement banner, maintenance mode toggle, and feature flags (`enable_resume_upload`, `enable_jd_analyzer`, `enable_expert_calls`).
- **`delete_user_account(user_id)`**: Deletes candidate accounts while preventing an administrator from deleting their own active session.

### `schemas.py`
- **`AdminLogin`**: Pydantic schema validating admin login requests (`email`, `password`).
- **`SiteSettingsUpdate`**: Pydantic schema allowing partial updates to:
  - `announcement_banner_text` (`str`)
  - `announcement_banner_visible` (`bool`)
  - `maintenance_mode` (`bool`)
  - `enable_resume_upload` (`bool`)
  - `enable_jd_analyzer` (`bool`)
  - `enable_expert_calls` (`bool`)

---

## 5. Security & Default Credentials

- **Default Administrator Account:** Seeded automatically on startup in `users_db.json`:
  - **Email:** `admin@careerpulse.ai`
  - **Password:** `admin123`
  - **Role:** `admin`
- All sensitive management operations enforce standard HTTP `401 Unauthorized` (missing/invalid token) and `403 Forbidden` (non-admin role) status codes.
