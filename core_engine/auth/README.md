# User Authentication & Session Management Subsystem

The `core_engine/auth` module powers user onboarding, secure credential authentication, role assignment (`user` vs. `admin`), and session persistence for **CareerPulse**.

---

## 1. Technical Stack & Security Architecture

- **Password Hashing:** Standard library `hashlib.pbkdf2_hmac` using **SHA-256** with **100,000 iterations** and a cryptographically secure 16-byte random salt generated via `secrets.token_hex(16)`.
- **Session Tokens:** Stateless **HMAC-SHA256 signed JWT tokens** with a 7-day expiration lifespan, encoded/decoded with native Python standard library modules (`base64`, `json`, `hmac`, `hashlib`, `time`).
- **Persistence Store:** Persistent JSON file database (`users_db.json`) ensuring zero external database overhead.
- **Default Roles:** Supports `user` (default for registered job candidates) and `admin` (system administrators).

---

## 2. API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/signup` | Registers a new candidate user account, hashes the password, and returns a 7-day JWT token | No |
| `POST` | `/api/v1/auth/login` | Authenticates existing user credentials, verifies PBKDF2 hash, and returns a JWT token | No |
| `GET` | `/api/v1/auth/me` | Validates Bearer token in the `Authorization` header and returns current user profile | Yes (Bearer Token) |

---

## 3. Directory Structure

```text
core_engine/auth/
├── README.md       # Subsystem documentation (this file)
├── __init__.py     # Package marker
├── router.py       # FastAPI router defining /signup, /login, and /me
├── schemas.py      # Pydantic schemas (UserCreate, UserLogin, UserResponse, TokenResponse)
├── service.py      # Core AuthService: PBKDF2 hashing, JWT signing, and user database CRUD
└── users_db.json   # Persistent JSON user store
```

---

## 4. Key Components

### `service.py` (`AuthService`)
- **`hash_password(password, salt)`**: Computes `hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)`.
- **`verify_password(password, salt, hashed)`**: Verifies candidate password input in constant time using `hmac.compare_digest`.
- **`create_access_token(user_id, email, role, expires_delta)`**: Generates a standard JWT token containing header, payload (`sub`, `email`, `role`, `exp`, `iat`), and HMAC-SHA256 signature.
- **`decode_access_token(token)`**: Decodes token, validates expiration, and verifies signature integrity using secret key.
- **`signup(data)`**: Validates uniqueness of email address, creates user entity, assigns `user` role, and persists to `users_db.json`.
- **`login(data)`**: Validates email and password, returning user profile and access token.
- **`get_user_from_token(token)`**: Extracts user ID from token and loads matching user record.
- **`delete_user(user_id)`**: Deletes user record from `users_db.json`.
- **`_init_default_admin()`**: Automatically seeds default admin account (`admin@careerpulse.ai` / `admin123`) if not present.

### `schemas.py`
- **`UserCreate`**: Request schema for user registration (`email`, `password`, `name`).
- **`UserLogin`**: Request schema for user authentication (`email`, `password`).
- **`UserResponse`**: Response schema containing public profile details (`id`, `email`, `name`, `role`, `created_at`).
- **`TokenResponse`**: Response schema containing `access_token`, `token_type` ("bearer"), and embedded `user` profile.

---

## 5. Default Administrative Account

Upon initial launch, the system automatically checks `users_db.json` and seeds the default administrator if missing:
- **Email:** `admin@careerpulse.ai`
- **Password:** `admin123`
- **Role:** `admin`
