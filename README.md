# Restaurant Management API

This project is a restaurant management backend built using FastAPI and PostgreSQL. It features a fully implemented token-based authentication system, robust data validation, and an automated database migration engine.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** Tortoise ORM
- **Migrations:** Aerich
- **Validation:** Pydantic v2
- **Security:** JWT (JSON Web Tokens) & Passlib (Bcrypt)
- **Testing:** Pytest & HTTPX AsyncClient

## Key Features

- **Database Schemas:** Models and relationships defined for Users, Restaurants, Owners, Addresses, Menu Items, Orders, and Order Items.
- **Authentication Layer:** Secure stateless architecture utilizing asymmetric access and refresh tokens.
- **Account Lifecycle:** Complete workflows for User Signup, Secure Login, Session Refresh, and Secure Logout.
- **Core Entities CRUD Management:** Comprehensive operational endpoints handling lifecycle workflows for Users, Addresses, and Restaurant Owners.
- **Immutable Address History Pattern:** Address updates do not overwrite historical records. Updates automatically soft-delete (deactivate) the current record and create a fresh active instance to preserve past order audit trails.
- **Automated Migrations:** Database schema tracking and state rollbacks managed entirely through Aerich.
- **Test Automation:** Fully isolated, asynchronous integration test suite running against transient in-memory SQLite instances.

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd FastApiAssignment
```

### 2. Install dependencies

```bash
uv sync
source .venv/bin/activate
```

### 3. Configure environment variables

Create a `.env` file in the project root directory and add your application settings:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your_password

JWT_SECRET_KEY=your_super_secret_signing_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Initialize Database Migrations

Before launching the server, initialize your database tables and tracking ledgers using Aerich:

```bash
# Initialize Aerich configuration
aerich init -t app.config.TORTOISE_ORM

# Create the initial schema migration script
aerich init-db

# (Optional) Apply outstanding schema modifications later on
# aerich migrate
# aerich upgrade
```

### 5. Run the Application

Start the live hot-reloading development server:

```bash
uvicorn main:app --reload
```

---

## API Reference

### 1. Authentication Layer (`/auth`)

| Method | Endpoint | Payload / Constraints | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/signup` | `username` (min 5 chars), `email`, `password` | Registers a fresh user profile and yields initial session tokens. |
| `POST` | `/auth/login` | `email`, `password` | Authenticates credentials and issues short-lived access tokens. |
| `POST` | `/auth/refresh` | Query params: `auth_uuid`, `user_id` | Validates a refresh token session to generate a new access token. |
| `POST` | `/auth/logout` | Query params: `auth_uuid` | Inactivates and removes the specific refresh-token session from the DB. |
| `POST` | `/auth/reactivate`| `email`, `password` | Reactivates a soft-deleted account profile and signs the user back in. |

### 2. User Profiles Management (`/users`)

| Method | Endpoint | Payload Constraints | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/users` | Admin Scope Required | Retrieves a master list of all database users ordered by their unique primary key ID. |
| `GET` | `/users/{id}` | Path param: `user_id` | Extracts a targeted user profile by its database index primary key. |
| `PUT` | `/users/{id}` | `username`, `email` (Optional fields) | Modifies permitted attributes on an active user profile, enforcing lowecase constraints. |
| `DELETE` | `/users/{id}` | Path param: `user_id`, `updated_by_id` | Soft-deletes a user profile by switching their status flag to inactive (`is_active=False`). |

### 3. Addresses Directory (`/addresses`)
*Manages geographical locations using an audit-safe historical mutation flow.*

| Method | Endpoint | Payload Constraints | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/addresses` | Implicitly scoped via active `user_id` | Retrieves all active (`is_active=True`) address records belonging to the authenticated user. |
| `POST` | `/addresses` | `street`, `city`, `house`, `zip`, `nearby_location`, `long`, `lat` | Attaches a fresh, validated address instance to the calling user profile. |
| `GET` | `/addresses/{id}` | Path param: `address_id` | Extracts detailed metrics for a targeted address if it is active and owned by the caller. |
| `PUT` | `/addresses/{id}` | `street`, `city`, `house`, `zip`, `nearby_location`, `long`, `lat` (All optional) | **History Patch:** Deactivates the existing record and spawns a new active instance with merged modifications. |

### 4. Owner Registry (`/owners`)

| Method | Endpoint | Payload Constraints | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/owners` | `user_id`, `restraunt_id` | Creates an ownership verification mapping linking a valid user to a valid restaurant. |
| `GET` | `/owners/{id}` | Path param: `owner_id` | Fetches a specific ownership association ledger record by its configuration ID. |

---

## Running the Test Suite

The project includes isolated async integration test workflows. Tests run automatically using an isolated, fast **in-memory SQLite configuration**, completely safe from mutating your production data store.

To execute the test module:

```bash
pytest app/test/test_auth.py -v
```

*Note: Global test behaviors—such as automatic async detection (`asyncio_mode = "auto"`) and loop scoping—are pre-configured in the project's root `pyproject.toml` configuration block.*

## API Documentation

Once your local server is up and running, you can explore the complete interactive OpenAPI schema representation at:

- **Interactive Swagger UI Layout:** `http://127.0.0`
- **Alternative ReDoc Visual Layout:** `http://127.0.0`
