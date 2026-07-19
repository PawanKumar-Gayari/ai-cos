"""
apps/core/utils/serialization.py

Universal JSON-safe serialization utilities.

Purpose:
- Safely serialize dataclasses
- Handle custom objects
- Prevent JSON serialization crashes
- Support Celery / Redis / API responses
- Production-safe recursive serialization

Usage:
    import json

    from apps.core.utils.serialization import safe_json_serializer

    json.dumps(data, default=safe_json_serializer)
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from pathlib import Path
from uuid import UUID


def safe_json_serializer(obj):
    """
    Universal production-safe JSON serializer.

    Supports:
    - dataclasses
    - custom classes with to_dict()
    - datetime/date
    - UUID
    - Decimal
    - Enum
    - set/frozenset
    - pathlib.Path
    - nested structures
    """

    # =====================================================
    # Custom serializer
    # =====================================================

    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        return obj.to_dict()

    # =====================================================
    # Dataclass support
    # =====================================================

    if is_dataclass(obj):
        return asdict(obj)

    # =====================================================
    # datetime/date
    # =====================================================

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    # =====================================================
    # UUID
    # =====================================================

    if isinstance(obj, UUID):
        return str(obj)

    # =====================================================
    # Decimal
    # =====================================================

    if isinstance(obj, Decimal):
        return float(obj)

    # =====================================================
    # Enum
    # =====================================================

    if isinstance(obj, Enum):
        return obj.value

    # =====================================================
    # Path
    # =====================================================

    if isinstance(obj, Path):
        return str(obj)

    # =====================================================
    # Sets
    # =====================================================

    if isinstance(obj, (set, frozenset)):
        return list(obj)

    # =====================================================
    # Objects with __dict__
    # =====================================================

    if hasattr(obj, "__dict__"):

        return {
            key: value
            for key, value in vars(obj).items()
            if not key.startswith("_")
        }

    # =====================================================
    # Final fallback
    # =====================================================

    return str(obj)
