# AI COS — AI Content Operating System

Enterprise-grade AI content generation and orchestration platform built with Django, Celery, Redis, Ollama, OpenAI, Gemini, semantic memory, monitoring, and intelligent routing.

---

# Features

## AI Generation

- Intelligent AI article generation
- Multi-provider LLM routing
- OpenAI support
- Gemini support
- Ollama local model support
- Provider fallback system
- Async generation pipeline
- SEO-aware generation engine
- Content scoring
- Response cleaning

---

## Memory System

- Semantic memory retrieval
- Session memory
- Hot memory layer
- Adaptive importance learning
- Usage tracking
- Persistent vector-style storage
- Context window building

---

## Monitoring

- System health monitoring
- Provider health tracking
- Metrics API
- Generation analytics
- Runtime diagnostics
- Cache monitoring

---

## Infrastructure

- Django REST Framework
- Celery async workers
- Redis caching
- PostgreSQL support
- Docker deployment
- NGINX reverse proxy
- Gunicorn production server
- OpenAPI documentation

---

# Architecture

```text
NGINX
↓
Gunicorn
↓
Django API
↓
LLM Router
↓
OpenAI / Gemini / Ollama
↓
Memory + Analytics + Monitoring
↓
Redis / PostgreSQL