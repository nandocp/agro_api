# Agro API

A FastAPI-based platform for rural property management, built with PostgreSQL, PostGIS, and SQLAlchemy.

## Background

This project sits at the intersection of two things I care about: agronomy and software development.

I am an Agronomic Engineering student and a Ruby on Rails developer. During a university vacation, I decided to learn Python - starting with [agro_tools](https://github.com/nandocp/agro_tools), a small project where I implemented agronomic calculation methods from subjects I was studying at the time, including photoperiod and evapotranspiration.

That experience led to a natural next step: building a full web API in Python. Since I was already in the agricultural domain, I decided to build something useful - a platform that allows landowners, leasers, and managers to manage their rural properties in a structured, traceable way.

## What This Is

Agro API is an API-only backend designed to support rural property management at multiple levels of complexity - from a small family farm tracking basic activities to a larger operation requiring livestock management, soil analysis, and supply chain traceability.

## Roadmap

The project is being built in phases:

**Phase 1 - Foundation (current)**
- Model core entities: accounts, estates, fields, activities, organisms, herds
- Implement endpoints for user interaction
- Establish multi-tenancy, RBAC, and event sourcing infrastructure

**Phase 2 - Frontend**
- Develop a frontend application consuming the API
- Offline-first support for field operations in low-connectivity rural environments
- Mobile-friendly for smartphones and tablets

**Phase 3 - Traceability**
- Record plantings on a private blockchain (Hyperledger or anchoring to a public chain) enabling full supply chain traceability
- Link harvest data - both perennial and annual crops - to geographic and blockchain records
- Support transport documentation (GTA, phytosanitary certificates) tied to traceable production records

## Planned Features

- **Planting management** - model complex arrangements including monocultures, intercropping rows, and broadcast seeding (muvuca); support both annual and perennial crops
- **Harvest tracking** - record yields linked to field geography and planting history
- **Livestock management** - track herds collectively or individually (SISBOV-compatible for export markets); support cattle, sheep, goats, poultry, swine, fish, and bees
- **Soil analysis** - store complete soil lab reports (chemical, physical, biological) linked to specific fields
- **Blockchain traceability** - immutable production records anchored externally for supply chain verification
- **Journal entries** - polymorphic narrative log attached to any entity in the system
- **Multi-tenancy** - full data isolation per account with plan-based quota enforcement
This is a personal project created by an **Agronomic Engineering student** who is also a developer.

## References

* https://medium.com/@notarious2/working-with-spatial-data-using-fastapi-and-geoalchemy-797d414d2fe7

## Tech Stack

- **Python 3.13+**
- **FastAPI** - REST API framework
- **SQLAlchemy 2.0** - async ORM with mapped dataclasses
- **PostgreSQL 18** + **PostGIS 3.6** - spatial database
- **Alembic** - database migrations
- **Pydantic v2** - data validation
- **psycopg** - async PostgreSQL driver

## Prerequisites

- [Fedora Toolbox](https://containertoolbx.org/) or compatible container environment
- [Podman](https://podman.io/) with rootless socket enabled
- PostgreSQL 18 + PostGIS running locally or in a container
- Python 3.13+
- [Poetry](https://python-poetry.org/)

## Getting Started

### 1. Clone and install dependencies
```bash
git clone
cd agro_api
poetry install
```

### 2. Enable Podman socket (required for test containers)
```bash
systemctl --user enable --now podman.socket
loginctl enable-linger $USER
```

### 3. Configure environment
Copy and edit the settings:
```bash
cp .env.example .env
```

Key variables:
```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/agro_db
ENVIRONMENT=development
SECRET_KEY=your-secret-key
SUPERADMIN_EMAIL=admin@system.com
SUPERADMIN_PASSWORD=changeme
```

### 4. Create and migrate the database
```bash
poetry run task db-create
poetry run task db-migrate
```

### 5. Run seeds
```bash
poetry run task db-seed
```

### 6. Start the development server
```bash
poetry run task dev
```

API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

## Development Workflow

## Development Environment
If your default shell is not bash and you are using Fedora Toolbox,
you may see a warning when entering the toolbox. This is expected and
does not affect functionality.

The toolbox will fall back to bash automatically.

### Available tasks
```bash
poetry run task dev            # start development server
poetry run task test           # run all tests
poetry run task test-unit      # run unit tests only (no database)
poetry run task lint           # lint with ruff
poetry run task format         # format with ruff
poetry run task db-migrate     # run migrations + dump schema + rebuild test image
poetry run task db-rollback    # rollback last migration
poetry run task db-reset       # reset database (downgrade + upgrade)
poetry run task seed           # run production seeds
poetry run task seed-dev       # run development fixtures
```

### Database migrations

When modifying models, generate a new migration:
```bash
poetry run alembic revision --autogenerate -m 'describe your change'
poetry run task db-migrate
```

`db-migrate` automatically:
1. Runs pending migrations
2. Dumps the updated schema to `migrations/schema.sql`
3. Dumps seed data to `migrations/seed_data.sql`
4. Rebuilds the test container image

### Running tests

Tests use [Testcontainers](https://testcontainers.com/) - Podman socket must be active.
```bash
# all tests
poetry run task test

# specific domain
poetry run pytest tests/domain/estates/

# with coverage
poetry run pytest --cov=app --cov-report=term-missing
```

Test isolation is handled via savepoints (`begin_nested`) - each test rolls back after execution without recreating the schema.

---
## Architecture

### Layered architecture
```
API Layer       → validates input, calls service, serializes response
Service Layer   → business rules, authorization, orchestration
Repository      → database queries (CRUDBase)
Model Layer     → SQLAlchemy mapped dataclasses
```

### Key conventions

- **Models** inherit from `ModelBase` - provides `id` (UUIDv7), `created_at`, `updated_at`
- **Enums** stored as `String` in database - validated by Pydantic at API layer
- **Geometries** stored as PostGIS types - WKT input/GeoJSON output at API layer
- **Relationships** use `lazy='raise'` - explicit loading required
- **Authorization** enforced via `@require_permission` decorator on service methods
- **Soft delete** - `archived_at` for estates/fields, `deactivated_at` for users

### Multi-tenancy

All data is scoped to an `Account` (tenant). Isolation is enforced at the service layer - every query filters by `account_id` derived from the authenticated user.

### Event sourcing

`EstateEvent` and `ActivityEvent` provide immutable audit logs with hash chaining for tamper detection. Events are published via `EventBus` from service methods.

---

## Authentication

JWT-based authentication with JTI invalidation for logout.
```
POST /auth/login    → returns access token
POST /auth/logout   → invalidates current token
POST /auth/refresh  → issues new token
```

Tokens expire after 8 hours (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`).

---
