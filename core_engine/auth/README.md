# User Authentication & Session Management Subsystem

The `core_engine/auth` module powers user onboarding, secure credential authentication, role assignment (`user` vs. `admin`), and session persistence for **CareerPulse**.

---

## 1. Technical Stack & Security Architecture

- **Password Hashing:** Standard library `hashlib.pbkdf2_hmac` using **SHA-256** with **100,000 iterations** and a cryptographically secure 16-byte random salt generated via `secrets.token_hex(16)`.
- **Session Tokens:** Stateless **HMAC-SHA256 signed JWT tokens** with a 7-day expiration lifespan, encoded/decoded with native Python standard library modules (`base64`, `json`, `hmac`, `hashlib`, `time`).
- **Persistence Store:** Persistent JSON file database (`users_db.json`) with strict corrupted-JSON integrity checks (raises `RuntimeError` on parse errors to prevent accidental data overwrites).
- **Default Roles:** Supports `user` (default for registered job candidates) and `admin` (system administrators).

---

## 2. API Endpoints

| Method | Endpoint | Description | Auth Required | Status Codes |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/signup` | Registers a new candidate user account, hashes the password, and returns a 7-day JWT token | No | `200`, `400`, `500` |
| `POST` | `/api/v1/auth/login` | Authenticates existing user credentials, verifies PBKDF2 hash, and returns a JWT token | No | `200`, `401`, `500` |
| `GET` | `/api/v1/auth/me` | Validates Bearer token in the `Authorization` header and returns current user profile | Yes (Bearer Token) | `200`, `401` |

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
- **`hash_password(password, salt=None)`**: Computes `hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)` with a 16-byte random salt if not provided.
- **`verify_password(password, pwd_hash, salt)`**: Verifies candidate password input in constant time using `hmac.compare_digest`.
- **`create_token(user_id, email, role="user")`**: Generates a standard JWT token containing header (`alg: HS256`, `typ: JWT`), payload (`sub`, `email`, `role`, `exp`), and HMAC-SHA256 signature.
- **`decode_token(token)`**: Validates HMAC signature integrity, checks expiration timestamp (`exp`), and returns the payload dictionary.
- **`signup(data, role="user")`**: Validates email uniqueness (case-insensitive), hashes the password, creates user record (`usr_<hex>`), and persists to `users_db.json`.
- **`login(data)`**: Authenticates email and password, returning user profile and access token.
- **`get_user_from_token(token)`**: Decodes token and retrieves matching user record from `users_db.json`.
- **`get_all_users()`**: Returns list of all registered users for administrative review.
- **`delete_user(user_id)`**: Deletes user record from `users_db.json`.
- **`_ensure_db()`**: Automatically seeds the default administrator account (`admin@careerpulse.ai` / `admin123`) on startup if not present.

### `schemas.py`
- **`UserCreate`**: Request schema for user registration (`full_name` $\ge 2$ chars, `email`, `password` $\ge 6$ chars).
- **`UserLogin`**: Request schema for user authentication (`email`, `password`).
- **`UserResponse`**: Response schema containing public profile details (`id`, `full_name`, `email`, `created_at`, `role`).
- **`TokenResponse`**: Response schema containing `access_token`, `token_type` ("bearer"), and embedded `UserResponse` profile.

---

## 5. Default Administrative Account

Upon initial launch, `AuthService` automatically verifies `users_db.json` and seeds the master administrator account if missing:
- **Email:** `admin@careerpulse.ai`
- **Password:** `admin123`
- **Role:** `admin`
