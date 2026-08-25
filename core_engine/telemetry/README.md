# Telemetry Analytics & Hardware Monitoring Subsystem

The `core_engine/telemetry` module provides real-time system hardware metrics, platform activity counters, audit event logging, and global site settings persistence for **CareerPulse**.

---

## 1. Technical Stack & Architecture

- **Hardware Telemetry:** `psutil` (Sampling real-time CPU %, RAM usage in MB / %, and backend uptime)
- **Activity Counters:** Tracks cumulative platform usage metrics (page views, parsed resumes, live WebRTC calls, job searches, JD analyses)
- **Event Audit Feed:** Maintains chronological activity logs (capped at latest 200 entries) with timestamps, event types, descriptions, and structured metadata
- **Persistence:** Local JSON file database (`telemetry_db.json`) with strict corrupted-JSON integrity checks (raises `RuntimeError` on parse errors to protect settings and logs)
- **Global Middleware:** Integrated with FastAPI request middleware in `core_engine/main.py` for automated page view recording and maintenance mode enforcement

---

## 2. Monitored Metrics & Settings

### System Hardware Load (`psutil`)
- **`cpu_usage_percent`**: Current CPU utilization percentage (`psutil.cpu_percent`)
- **`ram_usage_percent`**: Current memory percentage (`psutil.virtual_memory().percent`)
- **`ram_used_mb`**: RAM consumed in MB
- **`ram_total_mb`**: Total system RAM in MB
- **`uptime_seconds`**: Continuous backend server uptime in seconds (`psutil.boot_time()`)

### Activity Counters
- `total_page_views`: Total frontend page views and navigation requests
- `total_resume_analyses`: Total PDF resumes processed through `/api/v1/analyze`
- `total_expert_sessions`: Total WebRTC mentoring rooms initialized
- `total_job_searches`: Total semantic search queries evaluated
- `total_jd_evaluations`: Total direct JD match analyses run via `analyzer.html`

### Global Site Settings
- `announcement_banner`: Custom message displayed on top banner across all pages
- `announcement_active`: Boolean controlling banner visibility
- `maintenance_mode`: When `true`, non-admin API requests receive HTTP `503 Service Unavailable`
- `enable_resume_upload`: Feature toggle controlling `/api/v1/analyze`
- `enable_jd_analyzer`: Feature toggle for direct JD comparison tool
- `enable_expert_calls`: Feature toggle for WebRTC stage

---

## 3. Directory Structure

```text
core_engine/telemetry/
├── README.md           # Subsystem documentation (this file)
├── __init__.py         # Package marker
├── service.py          # TelemetryService: psutil sampling, event logging, settings management
└── telemetry_db.json   # Persistent JSON store for counters, settings, and audit logs
```

---

## 4. Key Methods (`TelemetryService`)

- **`log_event(event_type, description, metadata=None)`**: Appends a timestamped log entry to the persistent audit feed (capped at 200 recent entries) and automatically increments the matching activity counter:
  - `RESUME_ANALYSIS` $\to$ `total_resume_analyses`
  - `EXPERT_CALL_START` $\to$ `total_expert_sessions`
  - `JOB_SEARCH` $\to$ `total_job_searches`
  - `JD_ANALYZED` $\to$ `total_jd_evaluations`
  - `PAGE_VIEW` $\to$ `total_page_views`
  - Additional events: `ADMIN_LOGIN`, `USER_DELETED`, `SETTINGS_UPDATED`, `SYSTEM_STARTUP`, `LOGS_CLEARED`.
- **`get_settings()`**: Reads active site configuration from `telemetry_db.json`.
- **`update_settings(settings_update)`**: Updates site settings in `telemetry_db.json` and records a `SETTINGS_UPDATED` audit log entry.
- **`get_telemetry_summary(user_list=None)`**: Aggregates hardware load (`cpu_usage_percent`, `ram_usage_percent`, `ram_used_mb`, `ram_total_mb`, `uptime_seconds`), activity counters, settings, total registered users, and recent audit logs for the Admin Control Console (`/api/v1/admin/telemetry`).
- **`clear_logs()`**: Purges the audit log history upon administrator request and initializes a fresh `LOGS_CLEARED` event.
- **`_load_db()`**: Loads JSON data with explicit `RuntimeError` propagation on corruption to prevent accidental database wipes.
