from __future__ import annotations
from typing import Any
CONTENT_TYPES = ("Reel", "Carousel", "Post", "Story")

def optimize_content(*, content_type: str, title: str, metrics: dict[str, Any]) -> dict[str, Any]:
    normalized = content_type.title() if content_type else "Post"
    if normalized not in CONTENT_TYPES: normalized = "Post"
    rate = float(metrics.get("engagement_rate", 0) or 0); shares = int(metrics.get("shares", 0) or 0); saves = int(metrics.get("saves", 0) or 0)
    if rate >= 8 or shares + saves >= 25:
        strategy = "Scale this format"; hook = f"{title}: show the strongest benefit in the first 2 seconds."; cta = "Save this and share it with someone who needs it."
    elif rate >= 4:
        strategy = "Test a stronger variation"; hook = f"Stop scrolling: here's what makes {title} worth noticing."; cta = "Comment your take and save this for later."
    else:
        strategy = "Rework before repeating"; hook = f"3 quick reasons to check out {title}."; cta = "Follow for more useful tips and offers."
    length = "15–25 seconds" if normalized == "Reel" else "5–7 slides" if normalized == "Carousel" else "1 strong visual"
    return {"content_type": normalized, "strategy": strategy, "hook": hook, "cta": cta, "recommended_length": length}
