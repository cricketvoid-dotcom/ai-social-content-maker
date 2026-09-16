from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
PROVIDERS_PATH = ROOT / "providers.json"
STATE_PATH = ROOT / "auth-state.json"
PROFILE_DIR = ROOT / "profile"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def is_allowed(url: str, allowed_hosts: list[str]) -> bool:
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    return any(host == item or host.endswith("." + item) for item in allowed_hosts)


def choose_providers() -> list[str]:
    choices = {"1": "chatgpt", "2": "gemini", "3": "claude"}
    print("\nContentForge Browser Authorization")
    print("Choose the two AI accounts/sites you want to authorize:")
    print("1. ChatGPT")
    print("2. Gemini")
    print("3. Claude")
    raw = input("Enter two numbers separated by a comma (example: 1,2): ").strip()
    selected = [choices.get(item.strip()) for item in raw.split(",")]
    selected = [item for item in selected if item]
    if len(selected) != 2 or len(set(selected)) != 2:
        raise SystemExit("Please choose exactly two different providers.")
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Authorize two AI providers in ContentForge's dedicated Chrome profile."
    )
    parser.add_argument(
        "providers",
        nargs="*",
        choices=["chatgpt", "gemini", "claude"],
        help="Optional provider names. If omitted, an interactive two-provider selector is shown.",
    )
    args = parser.parse_args()

    selected = args.providers or choose_providers()
    if len(selected) != 2:
        parser.error("Choose exactly two providers.")
    if len(set(selected)) != 2:
        parser.error("Each provider can only be selected once.")

    config = load_json(CONFIG_PATH)
    providers = load_json(PROVIDERS_PATH)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)

    state = {
        "version": 1,
        "authorized_providers": [],
        "profile": "ContentForge Agent",
        "updated_at": None,
        "credentials_stored_by_app": False,
    }

    if STATE_PATH.exists():
        try:
            existing = load_json(STATE_PATH)
            if isinstance(existing, dict):
                state.update(existing)
        except json.JSONDecodeError:
            pass

    state["authorized_providers"] = [
        p for p in state["authorized_providers"] if p in providers
    ]

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=False,
            accept_downloads=True,
        )
        context.set_default_navigation_timeout(
            int(config.get("navigation_timeout_ms", 30000))
        )

        page = context.pages[0] if context.pages else context.new_page()

        def guard(route):
            if is_allowed(route.request.url, config["allowed_hosts"]):
                route.continue_()
            else:
                route.abort()

        page.route("**/*", guard)

        for provider_id in selected:
            provider = providers[provider_id]
            print(f"\nOpening {provider['name']} in the dedicated ContentForge Chrome profile...")
            page.goto(provider["url"], wait_until="domcontentloaded")
            print(f"{provider['name']} is open. Log in manually with the account you want ContentForge to use.")
            print("Do not send your password, verification code, cookies, or session data to ContentForge.")
            input(
                f"When you have finished signing in to {provider['name']}, press Enter here to authorize it... "
            )

            if provider_id not in state["authorized_providers"]:
                state["authorized_providers"].append(provider_id)

            state["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_state(state)
            print(f"Authorized locally: {provider['name']}")

        context.close()

    print("\nSetup complete.")
    print("Authorized providers:", ", ".join(state["authorized_providers"]) or "none")
    print(f"Dedicated Chrome profile: {PROFILE_DIR}")
    print("Passwords and login credentials are not written to auth-state.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
