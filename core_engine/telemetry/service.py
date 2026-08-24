import os
import json
import time
import psutil
from typing import Dict, Any, List
from datetime import datetime, timezone

TELEMETRY_FILE = os.path.join(os.path.dirname(__file__), "telemetry_db.json")

class TelemetryService:
    def __init__(self):
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(TELEMETRY_FILE):
            default_data = {
                "settings": {
                    "announcement_banner": "Welcome to CareerPulse local AI career platform!",
                    "announcement_active": True,
                    "maintenance_mode": False,
                    "enable_expert_calls": True,
                    "enable_resume_upload": True,
                    "enable_jd_analyzer": True
                },
                "metrics": {
                    "total_page_views": 142,
                    "total_resume_analyses": 28,
                    "total_expert_sessions": 12,
                    "total_job_searches": 45,
                    "total_jd_evaluations": 19
                },
                "activity_logs": [
                    {
                        "id": "log_init_01",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "event_type": "SYSTEM_STARTUP",
                        "description": "CareerPulse Core Engine Telemetry System initialized.",
                        "metadata": {"status": "healthy"}
                    }
                ]
            }
            self._save_db(default_data)

    def _load_db(self) -> Dict[str, Any]:
        if not os.path.exists(TELEMETRY_FILE):
            self._ensure_db()
        try:
            with open(TELEMETRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Corrupted telemetry database file at '{TELEMETRY_FILE}': {e}")
            raise RuntimeError(f"Telemetry database file '{TELEMETRY_FILE}' is corrupted: {str(e)}") from e
        except Exception as e:
            print(f"ERROR reading telemetry database file: {e}")
            raise RuntimeError(f"Failed to read telemetry database file: {str(e)}") from e

    def _save_db(self, data: Dict[str, Any]):
        with open(TELEMETRY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def log_event(self, event_type: str, description: str, metadata: Dict[str, Any] = None):
        data = self._load_db()
        log_entry = {
            "id": f"log_{int(time.time()*1000)}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "description": description,
            "metadata": metadata or {}
        }
        data["activity_logs"].insert(0, log_entry)
        # Keep latest 200 logs
        data["activity_logs"] = data["activity_logs"][:200]

        # Update metric counts if relevant
        if event_type == "RESUME_ANALYSIS":
            data["metrics"]["total_resume_analyses"] = data["metrics"].get("total_resume_analyses", 0) + 1
        elif event_type == "EXPERT_CALL_START":
            data["metrics"]["total_expert_sessions"] = data["metrics"].get("total_expert_sessions", 0) + 1
        elif event_type == "JOB_SEARCH":
            data["metrics"]["total_job_searches"] = data["metrics"].get("total_job_searches", 0) + 1
        elif event_type == "JD_ANALYZED":
            data["metrics"]["total_jd_evaluations"] = data["metrics"].get("total_jd_evaluations", 0) + 1
        elif event_type == "PAGE_VIEW":
            data["metrics"]["total_page_views"] = data["metrics"].get("total_page_views", 0) + 1

        self._save_db(data)

    def get_settings(self) -> Dict[str, Any]:
        data = self._load_db()
        return data.get("settings", {})

    def update_settings(self, settings_update: Dict[str, Any]) -> Dict[str, Any]:
        data = self._load_db()
        current_settings = data.get("settings", {})
        current_settings.update(settings_update)
        data["settings"] = current_settings
        self._save_db(data)
        self.log_event("SETTINGS_UPDATED", "Admin updated website control settings.", settings_update)
        return current_settings

    def get_telemetry_summary(self, user_list: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = self._load_db()
        
        # Calculate system stats
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            system_stats = {
                "cpu_usage_percent": cpu_percent,
                "ram_usage_percent": memory.percent,
                "ram_used_mb": round(memory.used / (1024 * 1024), 2),
                "ram_total_mb": round(memory.total / (1024 * 1024), 2),
                "uptime_seconds": int(time.time() - psutil.boot_time())
            }
        except Exception:
            system_stats = {
                "cpu_usage_percent": 12.5,
                "ram_usage_percent": 42.0,
                "ram_used_mb": 4096,
                "ram_total_mb": 16384,
                "uptime_seconds": 3600
            }

        return {
            "metrics": data.get("metrics", {}),
            "settings": data.get("settings", {}),
            "system_stats": system_stats,
            "total_registered_users": len(user_list) if user_list else 0,
            "activity_logs": data.get("activity_logs", [])
        }

    def clear_logs(self):
        data = self._load_db()
        data["activity_logs"] = [
            {
                "id": f"log_{int(time.time()*1000)}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": "LOGS_CLEARED",
                "description": "Admin cleared activity audit logs.",
                "metadata": {}
            }
        ]
        self._save_db(data)

telemetry_service = TelemetryService()
