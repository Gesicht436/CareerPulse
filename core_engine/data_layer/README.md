# Data Layer Module

## Overview

Handles all data persistence, database schemas, and data access patterns.

## Responsibilities

- **Schema Definition:** SQLAlchemy / SQLModel classes for Users, Resumes, Jobs.
- **Migrations:** Alembic scripts to manage DB state.
- **Data Access:** Helper functions to save/load data.
- **Validation:** Pydantic models shared across the application.

## Key Components

- `models.py`: Database tables.
- `schemas.py`: Pydantic data transfer objects.
- `db.py`: Database connection logic.

## Dependencies

- SQLAlchemy / SQLModel
- Pydantic
- Alembic
- PostgreSQL Driver (psycopg2)
