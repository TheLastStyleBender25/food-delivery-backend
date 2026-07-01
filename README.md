# Food Delivery Backend

A production-style microservices backend for a food delivery platform
built with FastAPI and modern backend infrastructure.

## Tech Stack

-   FastAPI
-   PostgreSQL
-   Redis
-   RabbitMQ
-   Celery
-   Docker & Docker Compose
-   SQLAlchemy
-   Alembic
-   JWT Authentication

## Auth Service Features

-   User Registration
-   Login & Logout
-   JWT Access and Refresh Tokens
-   Email Verification
-   Forgot Password Flow
-   OTP-based Password Reset
-   Role-based Users
-   Redis Rate Limiting
-   Background Email Tasks with Celery
-   Integration Tests with Pytest

## Running Locally

``` bash
docker compose up --build
```

Run migrations:

``` bash
alembic upgrade head
```

Swagger:

``` text
http://localhost:8000/docs
```

## Testing

``` bash
pytest tests -v
```
