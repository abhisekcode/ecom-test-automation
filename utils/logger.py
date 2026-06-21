"""Centralized logger; writes to a per-run, per-xdist-worker log file."""

import logging
import os

from utils.paths import PROJECT_ROOT

_LOGGER_NAME = "framework"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(_LOGGER_NAME)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        run_id = os.getenv("RUN_ID", "adhoc")
        worker = os.getenv("PYTEST_XDIST_WORKER", "main")
        log_dir = PROJECT_ROOT / "logs" / run_id
        log_dir.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_dir / f"{worker}.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
