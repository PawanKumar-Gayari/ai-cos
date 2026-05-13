#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
"""

import os
import sys


def main():
    """
    Run administrative tasks.
    """

    # Default settings module
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        os.getenv(
            "DJANGO_SETTINGS_MODULE",
            "config.settings.dev"
        )
    )

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exc:
        raise ImportError(
            "\nCouldn't import Django.\n"
            "Make sure:\n"
            "1. Django is installed\n"
            "2. Virtual environment is activated\n"
            "3. Requirements are installed\n"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()