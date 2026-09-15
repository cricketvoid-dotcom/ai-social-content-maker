from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

STATUSES = ("Planned", "Scheduled", "Published")

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def make_schedule_item(*, calendar_item: dict[str, Any], scheduled_at: str | None = None) -> dict[str, Any]:
    title = calendar_item.get("title", "Untitled")
    return {"id": f"sched-{calendar_item.get('date','')}-{title.lower().replace(' ', '-')[:24]}", "date": calendar_item.get("date", ""), "content_type": calendar_item.get("content_type", "Post"), "title": title, "concept": calendar_item.get("concept", ""), "scheduled_at": scheduled_at or calendar_item.get("date", ""), "status": "Scheduled", "created_at": _now()}

def calculate_analytics(*, impressions: int = 0, reach: int = 0, likes: int = 0, comments: int = 0, shares: int = 0, saves: int = 0, clicks: int = 0) -> dict[str, Any]:
    values = {"impressions": impressions, "reach": reach, "likes": likes, "comments": comments, "shares": shares, "saves": saves, "clicks": clicks}
    values = {k: max(0, int(v)) for k, v in values.items()}
    engagements = values["likes"] + values["comments"] + values["shares"] + values["saves"]
    base = values["reach"] or values["impressions"]
    return {**values, "engagements": engagements, "engagement_rate": round(engagements / base * 100, 2) if base else 0.0, "click_rate": round(values["clicks"] / base * 100, 2) if base else 0.0}

def performance_recommendation(*, metrics: dict[str, Any]) -> dict[str, Any]:
    rate = float(metrics.get("engagement_rate", 0)); shares = int(metrics.get("shares", 0)); saves = int(metrics.get("saves", 0))
    if rate >= 8 or shares + saves >= 25:
        return {"signal": "strong", "recommendation": "Create more content in this format and repeat its strongest hook."}
    if rate >= 4:
        return {"signal": "promising", "recommendation": "Keep the format, but test a stronger opening hook and clearer CTA."}
    return {"signal": "needs_testing", "recommendation": "Test a different hook, shorter opening, and a more specific CTA before scaling this format."}
