from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Dict, Any
from core_engine.auth.service import auth_service
from core_engine.auth.schemas import UserLogin, UserResponse, TokenResponse
from core_engine.admin.schemas import AdminLogin, SiteSettingsUpdate
from core_engine.telemetry.service import telemetry_service

router = APIRouter()

def get_current_admin(authorization: Optional[str] = Header(None)) -> UserResponse:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Admin authorization token missing.")
    
    token = authorization.split(" ")[1]
    user = auth_service.get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token.")
    
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden. Admin privileges required.")
    
    return user

@router.post("/login", response_model=TokenResponse)
async def admin_login(data: AdminLogin):
    try:
        user_resp, token = auth_service.login(UserLogin(email=data.email, password=data.password))
        if user_resp.role != "admin":
            raise HTTPException(status_code=403, detail="Access denied. Account is not an administrator.")
        
        telemetry_service.log_event("ADMIN_LOGIN", f"Admin {user_resp.email} logged into control console.", {"admin_id": user_resp.id})
        return TokenResponse(access_token=token, token_type="bearer", user=user_resp)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_admin_me(current_admin: UserResponse = Depends(get_current_admin)):
    return current_admin

@router.get("/telemetry")
async def get_telemetry_data(current_admin: UserResponse = Depends(get_current_admin)):
    users = auth_service.get_all_users()
    telemetry_data = telemetry_service.get_telemetry_summary(user_list=users)
    return telemetry_data

@router.get("/settings")
async def get_site_settings():
    return telemetry_service.get_settings()

@router.post("/settings")
async def update_site_settings(
    settings_data: SiteSettingsUpdate,
    current_admin: UserResponse = Depends(get_current_admin)
):
    update_dict = {k: v for k, v in settings_data.dict().items() if v is not None}
    updated = telemetry_service.update_settings(update_dict)
    return {"message": "Website settings updated successfully.", "settings": updated}

@router.get("/users")
async def list_registered_users(current_admin: UserResponse = Depends(get_current_admin)):
    users = auth_service.get_all_users()
    return {"users": users, "total": len(users)}

@router.delete("/users/{user_id}")
async def delete_user_account(
    user_id: str,
    current_admin: UserResponse = Depends(get_current_admin)
):
    if user_id == current_admin.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own active admin account.")
    
    success = auth_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User account not found.")
    
    telemetry_service.log_event("USER_DELETED", f"Admin deleted user account {user_id}.", {"user_id": user_id, "admin_id": current_admin.id})
    return {"message": f"User account {user_id} deleted successfully."}

@router.post("/clear-logs")
async def clear_telemetry_logs(current_admin: UserResponse = Depends(get_current_admin)):
    telemetry_service.clear_logs()
    return {"message": "Telemetry activity logs cleared."}
