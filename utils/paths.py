"""Filesystem anchors so paths don't depend on the process's working directory."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
