"""
JSON-based persistent memory storage.
"""

import json
import logging
import threading

from pathlib import Path
from tempfile import NamedTemporaryFile


logger = logging.getLogger(
    __name__
)


class JsonStore:

    DEFAULT_DATA = []

    def __init__(
        self,
        filename="memory_store.json",
    ):

        self.storage_path = (

            Path(__file__)
            .resolve()
            .parent
            / filename
        )

        self.backup_path = (
            self.storage_path.with_suffix(
                ".backup.json"
            )
        )

        # ==========================================
        # THREAD LOCK
        # ==========================================

        self._lock = (
            threading.Lock()
        )

        self._ensure_file_exists()

    # ==================================================
    # ENSURE FILE
    # ==================================================

    def _ensure_file_exists(
        self
    ):

        """
        Ensure storage file exists.
        """

        if not self.storage_path.exists():

            logger.info(
                "Creating JSON store."
            )

            self.save(
                self.DEFAULT_DATA
            )

    # ==================================================
    # VALID DATA
    # ==================================================

    def valid_data(
        self,
        data,
    ):

        """
        Validate JSON structure.
        """

        return isinstance(
            data,
            list,
        )

    # ==================================================
    # LOAD
    # ==================================================

    def load(
        self
    ):

        """
        Safe JSON load.
        """

        with self._lock:

            try:

                if not (
                    self.storage_path.exists()
                ):

                    return (
                        self.DEFAULT_DATA
                    )

                if (
                    self.storage_path.stat().st_size
                    == 0
                ):

                    logger.warning(
                        "Empty JSON store detected."
                    )

                    return (
                        self.DEFAULT_DATA
                    )

                with open(

                    self.storage_path,

                    "r",

                    encoding="utf-8",
                ) as file:

                    data = json.load(
                        file
                    )

                if not self.valid_data(
                    data
                ):

                    logger.warning(
                        "Invalid JSON structure."
                    )

                    return (
                        self.DEFAULT_DATA
                    )

                return data

            except json.JSONDecodeError:

                logger.exception(
                    "JSON corruption detected."
                )

                return self.restore_backup()

            except Exception as error:

                logger.exception(

                    f"JSON load failed: "
                    f"{str(error)}"
                )

                return (
                    self.DEFAULT_DATA
                )

    # ==================================================
    # SAVE
    # ==================================================

    def save(
        self,
        data,
    ):

        """
        Atomic JSON save.
        """

        with self._lock:

            try:

                if not self.valid_data(
                    data
                ):

                    logger.warning(
                        "Invalid save payload."
                    )

                    return False

                # ==========================================
                # BACKUP EXISTING FILE
                # ==========================================

                if self.storage_path.exists():

                    try:

                        self.backup_path.write_text(

                            self.storage_path.read_text(

                                encoding="utf-8"
                            ),

                            encoding="utf-8",
                        )

                    except Exception:

                        pass

                # ==========================================
                # ATOMIC WRITE
                # ==========================================

                with NamedTemporaryFile(

                    mode="w",

                    delete=False,

                    encoding="utf-8",
                ) as temp_file:

                    json.dump(

                        data,

                        temp_file,

                        indent=4,

                        ensure_ascii=False,
                    )

                    temp_path = Path(
                        temp_file.name
                    )

                temp_path.replace(
                    self.storage_path
                )

                return True

            except Exception as error:

                logger.exception(

                    f"JSON save failed: "
                    f"{str(error)}"
                )

                return False

    # ==================================================
    # RESTORE BACKUP
    # ==================================================

    def restore_backup(
        self
    ):

        """
        Restore backup JSON.
        """

        try:

            if not (
                self.backup_path.exists()
            ):

                logger.warning(
                    "No backup available."
                )

                return (
                    self.DEFAULT_DATA
                )

            with open(

                self.backup_path,

                "r",

                encoding="utf-8",
            ) as file:

                data = json.load(
                    file
                )

            if not self.valid_data(
                data
            ):

                return (
                    self.DEFAULT_DATA
                )

            logger.warning(
                "JSON backup restored."
            )

            return data

        except Exception as error:

            logger.exception(

                f"Backup restore failed: "
                f"{str(error)}"
            )

            return (
                self.DEFAULT_DATA
            )

    # ==================================================
    # FILE SIZE
    # ==================================================

    def file_size(
        self
    ):

        """
        Return storage file size.
        """

        try:

            if not (
                self.storage_path.exists()
            ):

                return 0

            return (
                self.storage_path
                .stat()
                .st_size
            )

        except Exception:

            return 0

    # ==================================================
    # CLEAR
    # ==================================================

    def clear(
        self
    ):

        """
        Clear JSON store.
        """

        logger.warning(
            "Clearing JSON store."
        )

        return self.save(
            self.DEFAULT_DATA
        )

    # ==================================================
    # STORAGE STATS
    # ==================================================

    def stats(
        self
    ):

        """
        Return storage statistics.
        """

        data = self.load()

        return {

            "items": len(data),

            "storage_file": str(
                self.storage_path
            ),

            "backup_file": str(
                self.backup_path
            ),

            "file_size_bytes": (
                self.file_size()
            ),

            "healthy": True,
        }