import os
import json
import hashlib
import hmac
import secrets
import base64
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from core_engine.auth.schemas import UserCreate, UserLogin, UserResponse

DB_FILE = os.path.join(os.path.dirname(__file__), "users_db.json")
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "careerpulse_super_secret_auth_key_2026")

class AuthService:
    def __init__(self):
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, "w", encoding="utf-8") as f:
                json.dump({}, f)
        
        # Ensure default admin account exists
        users = self._load_users()
        admin_email = "admin@careerpulse.ai"
        has_admin = any(u.get("role") == "admin" or u.get("email") == admin_email for u in users.values())
        
        if not has_admin:
            pwd_hash, salt = self.hash_password("admin123")
            admin_id = "usr_admin_master"
            users[admin_id] = {
                "id": admin_id,
                "full_name": "System Administrator",
                "email": admin_email,
                "password_hash": pwd_hash,
                "salt": salt,
                "role": "admin",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            self._save_users(users)

    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_users(self, users: Dict[str, Dict[str, Any]]):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        if not salt:
            salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return pwd_hash, salt

    def verify_password(self, password: str, pwd_hash: str, salt: str) -> bool:
        computed_hash, _ = self.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, pwd_hash)

    def create_token(self, user_id: str, email: str, role: str = "user") -> str:
        payload = {
            "sub": user_id,
            "email": email,
            "role": role,
            "exp": int(time.time()) + (86400 * 7)  # 7 days expiration
        }
        header_bytes = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).rstrip(b'=')
        payload_bytes = base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b'=')
        message = f"{header_bytes.decode('utf-8')}.{payload_bytes.decode('utf-8')}"
        signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        sig_bytes = base64.urlsafe_b64encode(signature).rstrip(b'=')
        return f"{message}.{sig_bytes.decode('utf-8')}"

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            header_str, payload_str, sig_str = parts
            message = f"{header_str}.{payload_str}"
            expected_sig = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
            expected_sig_bytes = base64.urlsafe_b64encode(expected_sig).rstrip(b'=').decode('utf-8')
            if not hmac.compare_digest(expected_sig_bytes, sig_str):
                return None
            
            padding = '=' * (4 - len(payload_str) % 4)
            payload_json = base64.urlsafe_b64decode(payload_str + padding).decode('utf-8')
            payload = json.loads(payload_json)
            
            if payload.get("exp", 0) < time.time():
                return None  # Expired
            return payload
        except Exception as e:
            print(f"DEBUG AuthService token decode error: {e}")
            return None

    def signup(self, data: UserCreate, role: str = "user") -> tuple[UserResponse, str]:
        users = self._load_users()
        email_clean = data.email.strip().lower()

        # Check if email exists
        for u in users.values():
            if u["email"].lower() == email_clean:
                raise ValueError("An account with this email already exists.")

        user_id = f"usr_{secrets.token_hex(8)}"
        pwd_hash, salt = self.hash_password(data.password)
        created_at = datetime.now(timezone.utc).isoformat()

        user_entry = {
            "id": user_id,
            "full_name": data.full_name.strip(),
            "email": email_clean,
            "password_hash": pwd_hash,
            "salt": salt,
            "role": role,
            "created_at": created_at
        }
        users[user_id] = user_entry
        self._save_users(users)

        user_resp = UserResponse(
            id=user_id,
            full_name=user_entry["full_name"],
            email=user_entry["email"],
            created_at=user_entry["created_at"],
            role=role
        )
        token = self.create_token(user_id, email_clean, role)
        return user_resp, token

    def login(self, data: UserLogin) -> tuple[UserResponse, str]:
        users = self._load_users()
        email_clean = data.email.strip().lower()

        target_user = None
        for u in users.values():
            if u["email"].lower() == email_clean:
                target_user = u
                break

        if not target_user:
            raise ValueError("Invalid email or password.")

        if not self.verify_password(data.password, target_user["password_hash"], target_user["salt"]):
            raise ValueError("Invalid email or password.")

        role = target_user.get("role", "user")

        user_resp = UserResponse(
            id=target_user["id"],
            full_name=target_user["full_name"],
            email=target_user["email"],
            created_at=target_user["created_at"],
            role=role
        )
        token = self.create_token(target_user["id"], target_user["email"], role)
        return user_resp, token

    def get_user_from_token(self, token: str) -> Optional[UserResponse]:
        payload = self.decode_token(token)
        if not payload:
            return None
        user_id = payload.get("sub")
        users = self._load_users()
        u = users.get(user_id)
        if not u:
            return None
        return UserResponse(
            id=u["id"],
            full_name=u["full_name"],
            email=u["email"],
            created_at=u["created_at"],
            role=u.get("role", "user")
        )

    def get_all_users(self) -> List[Dict[str, Any]]:
        users = self._load_users()
        user_list = []
        for u in users.values():
            user_list.append({
                "id": u["id"],
                "full_name": u["full_name"],
                "email": u["email"],
                "role": u.get("role", "user"),
                "created_at": u["created_at"]
            })
        return user_list

    def delete_user(self, user_id: str) -> bool:
        users = self._load_users()
        if user_id in users:
            del users[user_id]
            self._save_users(users)
            return True
        return False

auth_service = AuthService()
