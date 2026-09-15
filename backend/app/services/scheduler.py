from __future__ import annotations
from datetime import datetime, timezone
from typing import Any


def create_job(*, provider: str, account_name: str, content: dict[str, Any], scheduled_at: str | None = None) -> dict[str, Any]:
    when = scheduled_at or datetime.now(timezone.utc).isoformat()
    return {
        "job_id": f"job-{provider.lower().replace(' ', '-')}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
        "provider": provider,
        "account_name": account_name,
        "content": content,
        "scheduled_at": when,
        "status": "queued",
        "attempts": 0,
    }


def retry_job(job: dict[str, Any], *, error: str) -> dict[str, Any]:
    updated = dict(job)
    updated["attempts"] = int(updated.get("attempts", 0)) + 1
    updated["last_error"] = error
    updated["status"] = "retrying" if updated["attempts"] < 3 else "failed"
    return updated
