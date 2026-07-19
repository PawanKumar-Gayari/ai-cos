# ==================================================
# BASE IMAGE
# ==================================================

FROM python:3.12-slim


# ==================================================
# ENVIRONMENT
# ==================================================

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

ENV PIP_NO_CACHE_DIR=1


# ==================================================
# SYSTEM DEPENDENCIES
# ==================================================

RUN apt-get update && apt-get install -y \

    build-essential \

    gcc \

    curl \

    libpq-dev \

    && rm -rf /var/lib/apt/lists/*


# ==================================================
# WORK DIRECTORY
# ==================================================

WORKDIR /app


# ==================================================
# COPY REQUIREMENTS
# ==================================================

COPY requirements ./requirements


# ==================================================
# INSTALL PYTHON DEPENDENCIES
# ==================================================

RUN pip install --upgrade pip

RUN pip install -r requirements/prod.txt


# ==================================================
# COPY PROJECT
# ==================================================

COPY . .


# ==================================================
# STATIC FILES
# ==================================================

RUN mkdir -p /app/staticfiles

RUN mkdir -p /app/media


# ==================================================
# PORT
# ==================================================

EXPOSE 8000


# ==================================================
# HEALTHCHECK
# ==================================================

HEALTHCHECK --interval=30s \

  --timeout=10s \

  --start-period=20s \

  --retries=3 \

  CMD curl -f http://localhost:8000/api/monitoring/health/ || exit 1


# ==================================================
# START SERVER
# ==================================================

CMD [

  "gunicorn",

  "config.wsgi:application",

  "--bind",

  "0.0.0.0:8000",

  "--workers",

  "3",

  "--timeout",

  "300"
]