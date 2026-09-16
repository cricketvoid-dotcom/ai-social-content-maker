from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Authorize up to two AI providers in ContentForge's dedicated Chrome profile."
    )
    parser.add_argument(
        "providers",
        nargs="+",
        choices=["chatgpt", "gemini", "claude"],
        help="One or two providers to authorize.",
    )
    args = parser.parse_args()

    if len(args.providers) > 2:
        parser.error("Choose at most two providers.")
    if len(set(args.providers)) != len(args.providers):
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

    state["authorized_providers"] = [p for p in state["authorized_providers"] if p in providers]

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
            request_url = route.request.url
            from urllib.parse import urlparse
            host = (urlparse(request_url).hostname or "").lower().rstrip(".")
            allowed = any(host == h or host.endswith("." + h) for h in config["allowed_hosts"])
            if allowed:
                route.continue_()
            else:
                route.abort()

        page.route("**/*", guard)

        for provider_id in args.providers:
            provider = providers[provider_id]
            print(f"\nOpening {provider['name']} in the dedicated ContentForge Chrome profile...")
            page.goto(provider["url"], wait_until="domcontentloaded")
            print(f"{provider['name']} is open. Log in manually with the account you want ContentForge to use.")
            print("Do not send your password, verification code, cookies, or session data to ContentForge.")
            input(f"When you have finished signing in to {provider['name']}, press Enter here to authorize it... ")

            if provider_id not in state["authorized_providers"]:
                state["authorized_providers"].append(provider_id)

            state["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_state(state)
            print(f"Authorized locally: {provider['name']}")

        context.close()

    print("\nSetup complete.")
    print("Authorized providers:", ", ".join(state["authorized_providers"]) or "none")
    print(f"Session profile: {PROFILE_DIR}")
    print("Passwords and login credentials are not written to auth-state.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
