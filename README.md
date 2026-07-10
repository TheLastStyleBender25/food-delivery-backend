# Food Delivery Backend

A production-style **Food Delivery Backend** built using a **Microservices Architecture** with **FastAPI**. The project focuses on scalable backend design, asynchronous programming, secure authentication, inter-service communication, caching, background processing, containerization, and cloud deployment.

---

# Architecture

- Microservices Architecture
- Database per Service Pattern
- RESTful APIs
- Asynchronous Programming
- Repository Pattern
- Dependency Injection
- Cache Aside Pattern (Redis)
- Retry Pattern (Tenacity)
- Reverse Proxy (Nginx)

---

# Services

## ✅ Auth Service

Responsible for authentication and user management.

### Features

- User Registration
- User Login
- User Logout
- JWT Access Token
- JWT Refresh Token
- Refresh Token Rotation
- Email Verification
- Forgot Password
- OTP Based Password Reset
- Role Based Authentication
- Redis Rate Limiting
- Celery Background Tasks
- RabbitMQ Message Broker
- Integration Tests

---

## ✅ Restaurant Service

Responsible for restaurant management.

### Features

- Create Restaurant
- Update Restaurant
- Delete Restaurant
- Restaurant Ownership Validation
- Nearby Restaurant Search
- Customer Restaurant Listing
- Restaurant Pagination
- Restaurant Availability
- Geographical Filtering

---

## ✅ Menu Service

Responsible for restaurant menus.

### Features

- Create Menu Item
- Update Menu Item
- Delete Menu Item
- Restaurant Owner Authorization
- Customer Menu APIs
- Pagination
- Async SQLAlchemy
- Async Redis
- Async HTTP Client
- Redis Cache Aside
- Rate Limiting
- Retry with Tenacity
- Secure Image Upload
- Image Replacement
- Image Deletion
- Static Image Serving

### Image Upload Security

- UUID File Names
- File Extension Validation
- MIME Type Validation
- Image Content Validation (Pillow)
- File Size Validation
- Async File Upload (aiofiles)

---

# Technology Stack

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.0
- Async SQLAlchemy
- Pydantic v2
- Uvicorn

---

## Database

- PostgreSQL
- Alembic

---

## Cache

- Redis
- Async Redis Client

---

## Message Queue

- RabbitMQ

---

## Background Processing

- Celery

---

## Authentication & Security

- JWT Authentication
- Role Based Authorization
- Password Hashing (bcrypt)
- Redis Rate Limiting
- Input Validation
- Secure File Upload Validation

---

## HTTP & Service Communication

- HTTPX Async Client
- Tenacity Retry Mechanism
- Internal Service APIs

---

## File Storage

- Local File Storage
- Static File Serving
- Pillow
- aiofiles

---

## Testing

- Pytest
- pytest-asyncio
- HTTPX Test Client
- Dependency Overrides
- Monkeypatch
- Integration Testing

---

## DevOps

- Docker
- Docker Compose
- Nginx Reverse Proxy
- Let's Encrypt SSL
- AWS EC2 Deployment

---

# Infrastructure

```
                    Internet
                         │
                         ▼
                     Nginx (HTTPS)
                         │
      ┌──────────────────┼──────────────────┐
      │                  │                  │
      ▼                  ▼                  ▼
 Auth Service     Restaurant Service   Menu Service
      │                  │                  │
      └──────────────┬───┴──────────────┬───┘
                     │                  │
                     ▼                  ▼
               PostgreSQL          Redis
                     │
                     ▼
                 RabbitMQ
                     │
                     ▼
                  Celery
```

---

# Current Project Status

| Service | Status |
|----------|--------|
| ✅ Auth Service | Completed |
| ✅ Restaurant Service | Completed |
| ✅ Menu Service | Completed |
| ⏳ Cart Service | In Progress |
| ⏳ Order Service | Planned |
| ⏳ Payment Service | Planned |
| ⏳ Driver Service | Planned |

---

# Running Locally

Clone the repository

```bash
git clone <repository-url>
```

Start the application

```bash
docker compose up --build
```

Run database migrations

```bash
alembic upgrade head
```

---

# API Documentation

Auth Service

```
http://localhost:8000/docs
```

Restaurant Service

```
http://localhost:8001/docs
```

Menu Service

```
http://localhost:8002/docs
```

---

# Testing

Run all tests

```bash
pytest
```

Verbose output

```bash
pytest -v
```

---

# Deployment

The application is deployed on **AWS EC2** using Docker Compose with:

- Nginx Reverse Proxy
- Let's Encrypt SSL Certificates
- Docker Volumes
- PostgreSQL
- Redis
- RabbitMQ
- Celery Workers

---

# Upcoming Features

- Cart Service
- Order Service
- Payment Service
- Driver Service
- API Gateway
- Event Driven Communication
- Kafka Integration
- Kubernetes Deployment
