"""
Shared helper utilities for AI COS.
"""

import json

import re

import time

import uuid

from datetime import (

    datetime,

    timezone,
)


class Helpers:

    # ==================================================
    # CURRENT UTC TIMESTAMP
    # ==================================================

    @classmethod
    def current_timestamp(
        cls
    ):

        return (

            datetime.now(
                timezone.utc
            ).isoformat()
        )

    # ==================================================
    # CURRENT UNIX TIMESTAMP
    # ==================================================

    @classmethod
    def unix_timestamp(
        cls
    ):

        return int(
            time.time()
        )

    # ==================================================
    # GENERATE UUID
    # ==================================================

    @classmethod
    def generate_uuid(
        cls
    ):

        return str(
            uuid.uuid4()
        )

    # ==================================================
    # SAFE DICTIONARY GET
    # ==================================================

    @classmethod
    def safe_get(
        cls,
        data,
        key,
        default=None
    ):

        if not isinstance(
            data,
            dict
        ):

            return default

        return data.get(
            key,
            default
        )

    # ==================================================
    # SAFE INTEGER
    # ==================================================

    @classmethod
    def safe_int(
        cls,
        value,
        default=0
    ):

        try:

            return int(value)

        except (

            ValueError,

            TypeError
        ):

            return default

    # ==================================================
    # SAFE FLOAT
    # ==================================================

    @classmethod
    def safe_float(
        cls,
        value,
        default=0.0
    ):

        try:

            return float(value)

        except (

            ValueError,

            TypeError
        ):

            return default

    # ==================================================
    # SAFE DIVISION
    # ==================================================

    @classmethod
    def safe_divide(
        cls,
        numerator,
        denominator,
        default=0
    ):

        try:

            if denominator == 0:

                return default

            return (
                numerator
                / denominator
            )

        except Exception:

            return default

    # ==================================================
    # EXECUTION TIMER
    # ==================================================

    @classmethod
    def execution_timer(
        cls,
        start_time
    ):

        execution_time = (

            time.time()
            - start_time
        )

        return round(

            execution_time,

            4
        )

    # ==================================================
    # NORMALIZE TEXT
    # ==================================================

    @classmethod
    def normalize_text(
        cls,
        text
    ):

        if not text:

            return ""

        return (

            str(text)
            .strip()
            .lower()
        )

    # ==================================================
    # SLUGIFY TEXT
    # ==================================================

    @classmethod
    def slugify(
        cls,
        text
    ):

        if not text:

            return ""

        text = (

            str(text)
            .strip()
            .lower()
        )

        text = re.sub(

            r"[^a-z0-9\s-]",

            "",

            text
        )

        text = re.sub(

            r"\s+",

            "-",

            text
        )

        return text

    # ==================================================
    # STRING TO BOOLEAN
    # ==================================================

    @classmethod
    def to_bool(
        cls,
        value
    ):

        if isinstance(
            value,
            bool
        ):

            return value

        return str(
            value
        ).strip().lower() in [

            "true",

            "1",

            "yes",

            "y",

            "on"
        ]

    # ==================================================
    # IS EMPTY
    # ==================================================

    @classmethod
    def is_empty(
        cls,
        value
    ):

        return value in [

            None,

            "",

            [],

            {},

            ()
        ]

    # ==================================================
    # REMOVE DUPLICATES
    # ==================================================

    @classmethod
    def unique_list(
        cls,
        items
    ):

        if not items:

            return []

        return list(
            dict.fromkeys(items)
        )

    # ==================================================
    # FLATTEN NESTED LIST
    # ==================================================

    @classmethod
    def flatten_list(
        cls,
        nested_list
    ):

        if not nested_list:

            return []

        flat = []

        for item in nested_list:

            if isinstance(
                item,
                list
            ):

                flat.extend(
                    cls.flatten_list(
                        item
                    )
                )

            else:

                flat.append(item)

        return flat

    # ==================================================
    # CHUNK LIST
    # ==================================================

    @classmethod
    def chunk_list(
        cls,
        items,
        chunk_size=10
    ):

        if not items:

            return []

        if chunk_size <= 0:

            chunk_size = 10

        return [

            items[
                i:i + chunk_size
            ]

            for i in range(

                0,

                len(items),

                chunk_size
            )
        ]

    # ==================================================
    # LIMIT TEXT
    # ==================================================

    @classmethod
    def limit_text(
        cls,
        text,
        limit=200
    ):

        if not text:

            return ""

        text = str(text)

        if len(text) <= limit:

            return text

        return (

            text[:limit]
            .strip()

            + "..."
        )

    # ==================================================
    # FORMAT JSON
    # ==================================================

    @classmethod
    def pretty_json(
        cls,
        data
    ):

        return json.dumps(

            data,

            indent=4,

            ensure_ascii=False,

            default=str
        )

    # ==================================================
    # PERCENTAGE
    # ==================================================

    @classmethod
    def percentage(
        cls,
        value,
        total
    ):

        if total == 0:

            return 0

        return round(

            (
                value
                / total
            ) * 100,

            2
        )

    # ==================================================
    # MERGE DICTIONARIES
    # ==================================================

    @classmethod
    def merge_dicts(
        cls,
        *dicts
    ):

        merged = {}

        for item in dicts:

            if isinstance(
                item,
                dict
            ):

                merged.update(item)

        return merged