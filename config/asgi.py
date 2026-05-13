"""
ASGI config for ai_cos project.

It exposes the ASGI callable as a module-level variable named "application".
"""

import os

from django.core.asgi import get_asgi_application


# Default Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.dev"
    )
)

application = get_asgi_application()