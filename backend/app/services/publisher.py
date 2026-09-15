from __future__ import annotations

from typing import Any

from .connections import SUPPORTED_PROVIDERS, publish_dry_run


def validate_payload(*, provider: str, content: dict[str, Any]) -> dict[str, Any]:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError("Unsupported provider")
    if not content:
        raise ValueError("content must not be empty")
    return {"provider": provider, "valid": True, "content": content}


def publish(*, provider: str, account_name: str, content: dict[str, Any], dry_run: bool = True) -> dict[str, Any]:
    validate_payload(provider=provider, content=content)
    # V8 deliberately defaults to dry-run. Real publishing adapters must be
    # added only after OAuth scopes, platform review requirements, token
    # storage, retries, and platform-specific media rules are configured.
    if not dry_run:
        raise RuntimeError("Live publishing adapter is not configured; use dry_run=true")
    return publish_dry_run(provider=provider, account_name=account_name, content=content)
