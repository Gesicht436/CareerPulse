# Telemetry Analytics & Hardware Monitoring Subsystem

The `core_engine/telemetry` module provides real-time system metrics, platform activity counters, audit event logging, and global site settings persistence for **CareerPulse**.

---

## 1. Technical Stack & Architecture

- **Hardware Telemetry:** `psutil` (Sampling real-time CPU %, RAM usage in MB / %, and backend uptime)
- **Activity Counters:** Tracks cumulative platform usage metrics (page views, parsed resumes, live WebRTC calls, job searches, JD analyses)
- **Event Audit Feed:** Maintains chronological activity logs with timestamps, event types, and structured metadata
- **Persistence:** Local JSON file database (`telemetry_db.json`) for seamless zero-Docker configuration persistence
- **Global Middleware:** Integrated with FastAPI request middleware in `core_engine/main.py` for automated page view recording and maintenance mode enforcement

---

## 2. Monitored Metrics & Settings

### System Hardware Load
- **CPU Utilization:** Current CPU utilization percentage (`psutil.cpu_percent`)
- **Memory Consumption:** Total RAM, Used RAM in MB, and RAM percentage (`psutil.virtual_memory`)
- **System Uptime:** Continuous server uptime in seconds and human-readable formatted string

### Activity Counters
- `total_page_views`: Total frontend page views and navigation requests
- `total_resumes_analyzed`: Total PDF resumes processed through `/api/v1/analyze`
- `total_expert_calls`: Total WebRTC mentoring rooms initialized
- `total_job_searches`: Total semantic search queries evaluated
- `total_jd_evaluations`: Total direct JD match analyses run via `analyzer.html`

### Global Site Settings
- `announcement_banner_text`: Custom message displayed on top banner across all pages
- `announcement_banner_visible`: Boolean controlling banner visibility
- `maintenance_mode`: When `true`, non-admin API requests receive HTTP `503 Service Unavailable`
- `enable_resume_upload`: Feature toggle controlling `/api/v1/analyze`
- `enable_jd_analyzer`: Feature toggle for direct JD comparison tool
- `enable_expert_calls`: Feature toggle for WebRTC stage

---

## 3. Directory Structure

```text
core_engine/telemetry/
├── README.md           # Subsystem documentation (this file)
├── service.py          # TelemetryService: psutil sampling, event logging, settings management
└── telemetry_db.json   # Persistent JSON store for counters, settings, and audit logs
```

---

## 4. Key Methods (`TelemetryService`)

- **`get_system_metrics()`**: Samples current hardware telemetry via `psutil`.
- **`log_event(event_type, description, metadata)`**: Appends a timestamped log entry to the persistent audit feed (capped at 500 recent entries).
- **`get_settings()` / `update_settings(updates)`**: Reads and writes site settings in `telemetry_db.json`.
- **`increment_counter(counter_name)`**: Increments specific activity counters atomically.
- **`get_telemetry_summary(user_list)`**: Aggregates hardware load, activity counters, user metrics, and recent logs for the Admin Control Console (`/api/v1/admin/telemetry`).
- **`clear_logs()`**: Purges the audit log history upon administrator request.
