# My Project
# Restaurant Management API

This project is a restaurant management backend built using FastAPI and PostgreSQL. It is currently under development.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Tortoise ORM
- Aerich
- Pydantic
- JWT

## Current Progress

- Created database models for users, restaurants, addresses, menu items, orders, and order items.
- Defined relationships between database tables using Tortoise ORM.
- Created Pydantic schemas for user, restaurant, and order data validation.
- Added database configuration using environment variables.
- Configured PostgreSQL connection with Tortoise ORM.
- Set up Aerich for database migrations.
- Added JWT utilities for creating and validating access and refresh tokens.
- Started implementing user authentication and CRUD operations.

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

Create a `.env` file in the project root and configure your database and JWT settings.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=restaurant_db
DB_USER=postgres
DB_PASSWORD=your_password

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

### 5. API Documentation

Once the server is running, open:

- `http://127.0.0.1:8000/docs`

## Status

The project is under development. Database models, schemas, configuration, and JWT utility functions have been set up. API implementation and testing are ongoing.