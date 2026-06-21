"""Environment-aware configuration and credential loading."""

import json
import os

from utils.paths import PROJECT_ROOT

CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"

DEFAULT_USERNAME = "standard_user"
DEFAULT_PASSWORD = "secret_sauce"


def load_config() -> dict:
    """Return the config block for the active TEST_ENV (defaults to 'qa')."""
    env = os.getenv("TEST_ENV", "qa")

    with open(CONFIG_PATH) as f:
        all_config = json.load(f)

    return all_config[env]


def get_credentials() -> tuple[str, str]:
    """Return (username, password), preferring env vars over the SauceDemo demo defaults."""
    username = os.getenv("TEST_USERNAME", DEFAULT_USERNAME)
    password = os.getenv("TEST_PASSWORD", DEFAULT_PASSWORD)
    return username, password
