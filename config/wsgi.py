"""
WSGI config for ai_cos project.

It exposes the WSGI callable as a module-level variable named "application".
"""

import os

from django.core.wsgi import get_wsgi_application


# Default Django settings module
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv(
        "DJANGO_SETTINGS_MODULE",
        "config.settings.dev"
    )
)

application = get_wsgi_application()