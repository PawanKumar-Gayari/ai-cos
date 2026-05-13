"""
Enterprise session memory manager.
"""

import time
import logging
import threading

from datetime import datetime


logger = logging.getLogger(
    __name__
)


class SessionMemory:

    MAX_CONTEXT_ITEMS = 50

    SESSION_TTL = 86400

    MAX_VALUE_LENGTH = 5000

    _sessions = {}

    _lock = threading.Lock()

    # ==================================================
    # CURRENT TIME
    # ==================================================

    def now(
        self
    ):

        return time.time()

    # ==================================================
    # VALID SESSION ID
    # ==================================================

    def valid_session_id(
        self,
        session_id,
    ):

        """
        Validate session ID.
        """

        if not session_id:

            return False

        return True

    # ==================================================
    # CLEAN VALUE
    # ==================================================

    def clean_value(
        self,
        value,
    ):

        """
        Normalize session value.
        """

        if value is None:

            return ""

        value = str(
            value
        ).strip()

        if len(value) > (
            self.MAX_VALUE_LENGTH
        ):

            value = (
                value[
                    :self.MAX_VALUE_LENGTH
                ] + "..."
            )

        return value

    # ==================================================
    # SESSION EXPIRED
    # ==================================================

    def session_expired(
        self,
        session,
    ):

        """
        Check session expiration.
        """

        last_updated = session.get(
            "last_updated"
        )

        if not last_updated:

            return True

        elapsed = (
            self.now()
            - last_updated
        )

        return (
            elapsed > self.SESSION_TTL
        )

    # ==================================================
    # CLEANUP EXPIRED
    # ==================================================

    def cleanup_expired(
        self
    ):

        """
        Remove expired sessions.
        """

        with self._lock:

            expired_ids = []

            for session_id, session in (
                self._sessions.items()
            ):

                if self.session_expired(
                    session
                ):

                    expired_ids.append(
                        session_id
                    )

            for session_id in expired_ids:

                del self._sessions[
                    session_id
                ]

            if expired_ids:

                logger.info(

                    f"Removed "
                    f"{len(expired_ids)} "
                    f"expired sessions"
                )

            return len(
                expired_ids
            )

    # ==================================================
    # CREATE SESSION
    # ==================================================

    def create_session(
        self,
        session_id,
    ):

        """
        Create memory session.
        """

        if not self.valid_session_id(
            session_id
        ):

            return None

        with self._lock:

            self.cleanup_expired()

            if session_id not in (
                self._sessions
            ):

                logger.info(

                    f"Creating session: "
                    f"{session_id}"
                )

                self._sessions[
                    session_id
                ] = {

                    "created_at": (

                        datetime.utcnow()
                        .isoformat()
                    ),

                    "last_updated": (
                        self.now()
                    ),

                    "context": {},
                }

            return (
                self._sessions[
                    session_id
                ]
            )

    # ==================================================
    # TRIM CONTEXT
    # ==================================================

    def trim_context(
        self,
        context,
    ):

        """
        Trim oversized context.
        """

        items = list(
            context.items()
        )

        if len(items) <= (
            self.MAX_CONTEXT_ITEMS
        ):

            return context

        trimmed_items = items[
            -self.MAX_CONTEXT_ITEMS:
        ]

        return dict(
            trimmed_items
        )

    # ==================================================
    # SET CONTEXT
    # ==================================================

    def set_context(
        self,
        session_id,
        key,
        value,
    ):

        """
        Store session context.
        """

        session = (
            self.create_session(
                session_id
            )
        )

        if not session:

            return False

        clean_key = str(
            key
        ).strip()

        clean_value = (
            self.clean_value(
                value
            )
        )

        with self._lock:

            context = session[
                "context"
            ]

            # ==========================================
            # DUPLICATE PREVENTION
            # ==========================================

            existing = context.get(
                clean_key
            )

            if existing == clean_value:

                return True

            context[
                clean_key
            ] = clean_value

            session[
                "context"
            ] = self.trim_context(
                context
            )

            session[
                "last_updated"
            ] = self.now()

            return True

    # ==================================================
    # GET CONTEXT
    # ==================================================

    def get_context(
        self,
        session_id,
        key,
        default=None,
    ):

        """
        Retrieve session context.
        """

        with self._lock:

            session = (
                self._sessions.get(
                    session_id,
                    {},
                )
            )

            return (

                session.get(
                    "context",
                    {}
                ).get(
                    key,
                    default,
                )
            )

    # ==================================================
    # FULL CONTEXT
    # ==================================================

    def full_context(
        self,
        session_id,
    ):

        """
        Return full session context.
        """

        with self._lock:

            session = (
                self._sessions.get(
                    session_id,
                    {},
                )
            )

            return dict(

                session.get(
                    "context",
                    {}
                )
            )

    # ==================================================
    # SESSION METADATA
    # ==================================================

    def session_metadata(
        self,
        session_id,
    ):

        """
        Return session metadata.
        """

        with self._lock:

            session = (
                self._sessions.get(
                    session_id
                )
            )

            if not session:

                return None

            return {

                "created_at": (
                    session.get(
                        "created_at"
                    )
                ),

                "last_updated": (
                    session.get(
                        "last_updated"
                    )
                ),

                "context_items": len(

                    session.get(
                        "context",
                        {},
                    )
                ),
            }

    # ==================================================
    # CLEAR SESSION
    # ==================================================

    def clear_session(
        self,
        session_id,
    ):

        """
        Remove session memory.
        """

        with self._lock:

            if session_id in (
                self._sessions
            ):

                del self._sessions[
                    session_id
                ]

                logger.info(

                    f"Session cleared: "
                    f"{session_id}"
                )

                return True

            return False

    # ==================================================
    # SESSION EXISTS
    # ==================================================

    def session_exists(
        self,
        session_id,
    ):

        """
        Check session existence.
        """

        with self._lock:

            return session_id in (
                self._sessions
            )

    # ==================================================
    # TOTAL SESSIONS
    # ==================================================

    def total_sessions(
        self
    ):

        """
        Return active sessions.
        """

        with self._lock:

            return len(
                self._sessions
            )

    # ==================================================
    # ALL SESSIONS
    # ==================================================

    def all_sessions(
        self
    ):

        """
        Return all sessions.
        """

        with self._lock:

            return dict(
                self._sessions
            )

    # ==================================================
    # SYSTEM STATS
    # ==================================================

    def stats(
        self
    ):

        """
        Session memory statistics.
        """

        return {

            "total_sessions": (
                self.total_sessions()
            ),

            "session_ttl": (
                self.SESSION_TTL
            ),

            "max_context_items": (
                self.MAX_CONTEXT_ITEMS
            ),

            "max_value_length": (
                self.MAX_VALUE_LENGTH
            ),
        }