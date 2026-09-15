import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(os.getenv("BRAND_DB_PATH", Path(__file__).resolve().parents[2] / "contentforge.db"))

FIELDS = (
    "business_name", "business_type", "tagline", "primary_color", "secondary_color",
    "accent_color", "font_family", "phone", "location", "social_handle", "logo_data",
)


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS brand_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            business_type TEXT NOT NULL,
            tagline TEXT NOT NULL DEFAULT '',
            primary_color TEXT NOT NULL DEFAULT '#171722',
            secondary_color TEXT NOT NULL DEFAULT '#ffffff',
            accent_color TEXT NOT NULL DEFAULT '#5146d8',
            font_family TEXT NOT NULL DEFAULT 'Inter',
            phone TEXT NOT NULL DEFAULT '',
            location TEXT NOT NULL DEFAULT '',
            social_handle TEXT NOT NULL DEFAULT '',
            logo_data TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )"""
    )
    conn.commit()
    return conn


def _row(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row else None


def list_brands() -> list[dict[str, Any]]:
    with _connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM brand_profiles ORDER BY updated_at DESC")]


def get_brand(brand_id: int) -> dict[str, Any] | None:
    with _connect() as conn:
        return _row(conn.execute("SELECT * FROM brand_profiles WHERE id = ?", (brand_id,)).fetchone())


def create_brand(data: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    values = [data.get(field, "") for field in FIELDS]
    with _connect() as conn:
        cur = conn.execute(
            f"INSERT INTO brand_profiles ({', '.join(FIELDS)}, created_at, updated_at) VALUES ({', '.join('?' for _ in FIELDS)}, ?, ?)",
            [*values, now, now],
        )
        conn.commit()
        return get_brand(int(cur.lastrowid)) or {}


def update_brand(brand_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
    current = get_brand(brand_id)
    if not current:
        return None
    merged = {field: data.get(field, current[field]) for field in FIELDS}
    now = datetime.now(timezone.utc).isoformat()
    assignments = ", ".join(f"{field} = ?" for field in FIELDS)
    with _connect() as conn:
        conn.execute(f"UPDATE brand_profiles SET {assignments}, updated_at = ? WHERE id = ?", [*[merged[field] for field in FIELDS], now, brand_id])
        conn.commit()
    return get_brand(brand_id)


def delete_brand(brand_id: int) -> bool:
    with _connect() as conn:
        cur = conn.execute("DELETE FROM brand_profiles WHERE id = ?", (brand_id,))
        conn.commit()
        return cur.rowcount > 0
