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

- **Database Schemas:** Models and relationships defined for Users, Restaurants, Addresses, Menu Items, Orders, and Order Items.
- **Authentication Layer:** Secure stateless architecture utilizing asymmetric access and refresh tokens.
- **Account Lifecycle:** Complete workflows for User Signup, Secure Login, Session Refresh, and Secure Logout.
- **Account Recovery:** Self-service account reactivation support for soft-deleted profiles.
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

## Authentication API Reference

All authentication endpoints are grouped under the `/auth` router prefix:

| Method | Endpoint | Payload Constraints | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/auth/signup` | `username` (min 5 chars), `email`, `password` | Registers a fresh user profile and yields initial session tokens. |
| `POST` | `/auth/login` | `email`, `password` | Authenticates credentials and issues short-lived access tokens. |
| `POST` | `/auth/refresh` | Query params: `auth_uuid`, `user_id` | Validates a refresh token session to generate a new access token. |
| `POST` | `/auth/logout` | Query params: `auth_uuid` | Invalidates and removes the specific refresh-token session from the DB. |
| `POST` | `/auth/reactivate`| `email`, `password` | Reactivates a soft-deleted account profile and signs the user back in. |

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

- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
- Alternative ReDoc Layout: `http://127.0.0`
