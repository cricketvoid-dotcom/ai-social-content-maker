from __future__ import annotations
from typing import Any

SUPPORTED_PLATFORMS = ("Instagram", "Facebook", "YouTube Shorts", "LinkedIn", "X")


def _clean(value: str, limit: int) -> str:
    return " ".join((value or "").split())[:limit]


def generate_platform_content(*, business_name: str, topic: str, base_caption: str = "", platforms: list[str] | None = None) -> dict[str, Any]:
    selected = platforms or list(SUPPORTED_PLATFORMS)
    selected = [p for p in selected if p in SUPPORTED_PLATFORMS]
    if not selected:
        selected = ["Instagram"]

    caption = _clean(base_caption, 1000) or f"{topic} — a useful update from {business_name}."
    results: dict[str, dict[str, Any]] = {}
    for platform in selected:
        if platform == "Instagram":
            results[platform] = {"caption": caption, "hashtags": ["#localbusiness", "#smallbusiness", "#discover"], "format": "Post or Reel", "cta": "Save this and follow for more."}
        elif platform == "Facebook":
            results[platform] = {"caption": _clean(caption, 1500), "hashtags": ["#localbusiness", "#smallbusiness"], "format": "Post", "cta": "Message us to learn more."}
        elif platform == "YouTube Shorts":
            results[platform] = {"title": _clean(topic, 90), "description": _clean(caption, 500), "hashtags": ["#Shorts", "#localbusiness"], "format": "Short", "cta": "Subscribe for more."}
        elif platform == "LinkedIn":
            results[platform] = {"caption": f"{topic}\n\n{caption}", "hashtags": ["#smallbusiness", "#business", "#growth"], "format": "Text or media post", "cta": "Share your perspective in the comments."}
        else:
            results[platform] = {"text": _clean(f"{topic} — {caption}", 280), "hashtags": ["#smallbusiness", "#localbusiness"], "format": "Post", "cta": "Follow for updates."}
    return {"business_name": business_name, "platforms": results}
