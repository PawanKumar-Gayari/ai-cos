# AI COS Publisher

Enterprise publishing system for AI COS.

Handles:

- WordPress publishing
- Draft creation
- Live publishing
- Retry workflows
- Publish tracking
- API integration
- Background tasks

---

# Architecture

```text
WordPress Plugin
        ↓
Publisher API
        ↓
Publisher Engine
        ↓
Publish Service
        ↓
WordPress Client
        ↓
WordPress REST API
```

---

# Features

## API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/publisher/health/` | GET | Health check |
| `/api/publisher/generate/` | POST | Generate article |
| `/api/publisher/publish/` | POST | Publish article |

---

# Models

## PublishedPost

Tracks:

- publish status
- retries
- WordPress post ID
- response data
- errors
- duration

---

# Services

## PublishService

Handles:

- article validation
- tracker creation
- WordPress publishing
- publish lifecycle

---

# Engine

## PublisherEngine

Central orchestration layer.

Responsible for:

- workflow management
- service coordination
- publishing execution

---

# Tasks

## retry_tasks.py

Retries failed publishing attempts.

## cleanup_tasks.py

Handles old failure cleanup.

## health_tasks.py

System reporting and health.

## publish_tasks.py

Background publishing.

---

# WordPress Integration

Uses:

- REST API
- Bearer authentication
- JSON communication

---

# Environment Variables

```env
WORDPRESS_URL=https://example.com
WORDPRESS_API_KEY=your_api_key
```

---

# Retry Strategy

- Maximum retries: 3
- Failed publishes tracked
- Error logging enabled

---

# Future Improvements

- Celery queue support
- Multi-site publishing
- Async workers
- Webhook events
- Analytics dashboard
- Scheduled publishing
- AI rewrite workflows

---

# Development

Run tests:

```bash
python manage.py test apps.publisher
```

---

# API Documentation

Swagger:

```text
/api/docs/
```

Redoc:

```text
/api/redoc/
```

---

# Status

Current state:

- API Ready
- Plugin Ready
- WordPress Ready
- Queue Ready
- SaaS Foundation Ready