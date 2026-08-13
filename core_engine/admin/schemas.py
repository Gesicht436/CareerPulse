from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class AdminLogin(BaseModel):
    email: str = Field(..., json_schema_extra={"example": "admin@careerpulse.ai"})
    password: str = Field(..., json_schema_extra={"example": "admin123"})

class SiteSettingsUpdate(BaseModel):
    announcement_banner: Optional[str] = None
    announcement_active: Optional[bool] = None
    maintenance_mode: Optional[bool] = None
    enable_expert_calls: Optional[bool] = None
    enable_resume_upload: Optional[bool] = None
    enable_jd_analyzer: Optional[bool] = None
