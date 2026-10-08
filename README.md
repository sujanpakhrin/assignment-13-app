# Assignment 13 — GitOps CI/CD

Three-tier containerized application for Assignment 13.

## Architecture

Frontend → Backend API → PostgreSQL

## Components

- Frontend: Nginx
- Backend: FastAPI
- Database: PostgreSQL
- Local orchestration: Docker Compose

## Local Run

```
docker compose up --build -d
```

Frontend:

http://localhost:90

Backend health:

http://localhost:8000/api/health

## Tests

```
cd backend
python -m pytest
```
