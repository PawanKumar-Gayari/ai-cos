"""
Central logging utility for AI COS.
"""

import logging

from logging.handlers import RotatingFileHandler

from pathlib import Path


# ==================================================
# LOG DIRECTORY
# ==================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

LOG_DIR = (
    BASE_DIR / "logs"
)

LOG_DIR.mkdir(
    exist_ok=True
)


# ==================================================
# LOG FILES
# ==================================================

APP_LOG_FILE = (
    LOG_DIR / "app.log"
)

ERROR_LOG_FILE = (
    LOG_DIR / "error.log"
)


# ==================================================
# LOG FORMAT
# ==================================================

LOG_FORMAT = (

    "[%(asctime)s] "
    "[%(levelname)s] "
    "[%(name)s] "
    "%(message)s"
)

DATE_FORMAT = (
    "%Y-%m-%d %H:%M:%S"
)


# ==================================================
# ROOT LOGGER CONFIG
# ==================================================

logging.basicConfig(

    level=logging.INFO,

    format=LOG_FORMAT,

    datefmt=DATE_FORMAT,
)


# ==================================================
# FILE HANDLERS
# ==================================================

app_handler = RotatingFileHandler(

    APP_LOG_FILE,

    maxBytes=5 * 1024 * 1024,

    backupCount=5,

    encoding="utf-8"
)

app_handler.setLevel(
    logging.INFO
)

app_handler.setFormatter(

    logging.Formatter(

        LOG_FORMAT,

        DATE_FORMAT
    )
)


error_handler = RotatingFileHandler(

    ERROR_LOG_FILE,

    maxBytes=5 * 1024 * 1024,

    backupCount=5,

    encoding="utf-8"
)

error_handler.setLevel(
    logging.ERROR
)

error_handler.setFormatter(

    logging.Formatter(

        LOG_FORMAT,

        DATE_FORMAT
    )
)


# ==================================================
# CONSOLE HANDLER
# ==================================================

console_handler = logging.StreamHandler()

console_handler.setLevel(
    logging.INFO
)

console_handler.setFormatter(

    logging.Formatter(

        LOG_FORMAT,

        DATE_FORMAT
    )
)


# ==================================================
# LOGGER FACTORY
# ==================================================

def get_logger(
    name="ai_cos"
):

    logger = logging.getLogger(
        name
    )

    # =========================
    # PREVENT DUPLICATES
    # =========================

    if not logger.handlers:

        logger.addHandler(
            app_handler
        )

        logger.addHandler(
            error_handler
        )

        logger.addHandler(
            console_handler
        )

        logger.setLevel(
            logging.INFO
        )

    return logger


# ==================================================
# GLOBAL LOGGER
# ==================================================

logger = get_logger()


# ==================================================
# PIPELINE LOGGER
# ==================================================

pipeline_logger = get_logger(
    "pipeline"
)


# ==================================================
# AI LOGGER
# ==================================================

ai_logger = get_logger(
    "ai"
)


# ==================================================
# SEO LOGGER
# ==================================================

seo_logger = get_logger(
    "seo"
)


# ==================================================
# COMPETITOR LOGGER
# ==================================================

competitor_logger = get_logger(
    "competitor"
)