"""
Celery configuration for AI COS.
"""

import os

from celery import Celery


# =========================
# DJANGO SETTINGS
# =========================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.dev"
)

# =========================
# CREATE CELERY APP
# =========================

app = Celery(
    "ai_cos"
)

# =========================
# LOAD DJANGO SETTINGS
# =========================

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY"
)

# =========================
# AUTO DISCOVER TASKS
# =========================

app.autodiscover_tasks()

# =========================
# DEBUG TASK
# =========================

@app.task(bind=True)
def debug_task(self):

    print(
        f"Request: {self.request!r}"
    )