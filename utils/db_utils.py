"""SQLite helpers for the cart table used by integration tests.

Each pytest-xdist worker gets its own database file so parallel runs
never contend for the same SQLite file/lock.
"""

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from utils.paths import PROJECT_ROOT


def _db_path() -> Path:
    worker = os.getenv("PYTEST_XDIST_WORKER", "main")
    suffix = "" if worker == "main" else f"_{worker}"
    return PROJECT_ROOT / f"ecom{suffix}.db"


@contextmanager
def _connection():
    conn = sqlite3.connect(_db_path())
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def create_cart_table() -> None:
    with _connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """)


def insert_product(product_name: str) -> None:
    create_cart_table()

    with _connection() as conn:
        conn.execute(
            "INSERT INTO cart (product_name, created_at) VALUES (?, ?)",
            (product_name, datetime.now().isoformat()),
        )


def clear_cart() -> None:
    create_cart_table()

    with _connection() as conn:
        conn.execute("DELETE FROM cart")


def get_products() -> list[str]:
    create_cart_table()

    with _connection() as conn:
        rows = conn.execute("SELECT product_name FROM cart").fetchall()

    return [row[0] for row in rows]
