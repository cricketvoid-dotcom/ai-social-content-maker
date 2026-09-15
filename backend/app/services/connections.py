from __future__ import annotations

import hashlib
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app.db"
SUPPORTED_PROVIDERS = ("Instagram", "Facebook", "YouTube", "LinkedIn", "X")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS social_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider TEXT NOT NULL,
            account_name TEXT NOT NULL,
            token_fingerprint TEXT NOT NULL,
            token_configured INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'connected',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )"""
    )
    return conn


def _fingerprint(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]


def list_connections() -> list[dict[str, Any]]:
    with _db() as conn:
        rows = conn.execute(
            "SELECT id, provider, account_name, token_configured, status, created_at, updated_at FROM social_connections ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def create_connection(*, provider: str, account_name: str, token: str) -> dict[str, Any]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider")
    if not account_name.strip():
        raise ValueError("account_name is required")
    if not token.strip():
        raise ValueError("A non-empty authorization token is required")
    now = _now()
    with _db() as conn:
        cur = conn.execute(
            "INSERT INTO social_connections(provider, account_name, token_fingerprint, token_configured, status, created_at, updated_at) VALUES (?, ?, ?, 1, 'connected', ?, ?)",
            (provider, account_name.strip(), _fingerprint(token), now, now),
        )
        row = conn.execute(
            "SELECT id, provider, account_name, token_configured, status, created_at, updated_at FROM social_connections WHERE id = ?",
            (cur.lastrowid,),
        ).fetchone()
    return dict(row)


def delete_connection(connection_id: int) -> bool:
    with _db() as conn:
        cur = conn.execute("DELETE FROM social_connections WHERE id = ?", (connection_id,))
    return cur.rowcount > 0


def publish_dry_run(*, provider: str, account_name: str, content: dict[str, Any]) -> dict[str, Any]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider")
    return {
        "mode": "dry_run",
        "provider": provider,
        "account_name": account_name,
        "status": "ready",
        "job_id": f"dry-{secrets.token_hex(6)}",
        "message": "Content validated locally. No social-platform request was sent.",
        "content": content,
    }
