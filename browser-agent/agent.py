from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
PROFILE_DIR = ROOT / "profile"
WORKSPACE_DIR = ROOT / "workspace"
INPUT_DIR = WORKSPACE_DIR / "input"
OUTPUT_DIR = WORKSPACE_DIR / "output"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def host_allowed(url: str, allowed_hosts: list[str]) -> bool:
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    for allowed in allowed_hosts:
        allowed = allowed.lower().rstrip(".")
        if host == allowed or host.endswith("." + allowed):
            return True
    return False


def ensure_workspace() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="ContentForge restricted Chrome agent")
    parser.add_argument("--url", required=True, help="Approved website URL to open")
    args = parser.parse_args()

    config = load_config()
    ensure_workspace()

    if not host_allowed(args.url, config["allowed_hosts"]):
        raise SystemExit(
            "Blocked: this host is not in browser-agent/config.json allowed_hosts."
        )

    with sync_playwright() as p:
        # `channel=chrome` uses the locally installed Google Chrome channel.
        # A separate user-data-dir prevents reuse of the user's normal Chrome profile.
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=bool(config.get("headless", False)),
            accept_downloads=True,
            downloads_path=str(OUTPUT_DIR),
        )
        context.set_default_navigation_timeout(
            int(config.get("navigation_timeout_ms", 30000))
        )

        page = context.pages[0] if context.pages else context.new_page()

        # Route-level guard: navigation to a non-allowlisted host is aborted.
        def guard(route):
            if host_allowed(route.request.url, config["allowed_hosts"]):
                route.continue_()
            else:
                route.abort()

        page.route("**/*", guard)
        page.goto(args.url, wait_until="domcontentloaded")
        print(f"Opened approved site: {page.url}")
        print("Restricted Chrome is running. Close the browser when finished.")
        page.wait_for_timeout(1000)

        # V1 deliberately stops here. Provider-specific upload/generate/download
        # actions will be implemented as explicit adapters rather than allowing
        # unrestricted browser control.
        context.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
