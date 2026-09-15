from __future__ import annotations
from collections import defaultdict
from typing import Any

CONTENT_TYPES = ("Reel", "Carousel", "Post", "Story")


def _safe_int(value: Any) -> int:
    try:
        return max(0, int(value or 0))
    except (TypeError, ValueError):
        return 0


def score_content(item: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic growth score from supplied performance metrics."""
    reach = _safe_int(item.get("reach")) or _safe_int(item.get("impressions"))
    likes = _safe_int(item.get("likes"))
    comments = _safe_int(item.get("comments"))
    shares = _safe_int(item.get("shares"))
    saves = _safe_int(item.get("saves"))
    clicks = _safe_int(item.get("clicks"))
    engagements = likes + comments + shares + saves
    engagement_rate = (engagements / reach * 100) if reach else 0.0
    share_save_rate = ((shares + saves) / reach * 100) if reach else 0.0
    click_rate = (clicks / reach * 100) if reach else 0.0
    score = min(100.0, engagement_rate * 6 + share_save_rate * 10 + click_rate * 4)
    return {"score": round(score, 2), "engagement_rate": round(engagement_rate, 2), "share_save_rate": round(share_save_rate, 2), "click_rate": round(click_rate, 2), "engagements": engagements}


def growth_insights(*, items: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize winning formats and turn metrics into actionable next steps."""
    scored = []
    format_scores: dict[str, list[float]] = defaultdict(list)
    for item in items:
        metrics = score_content(item)
        row = {**item, **metrics}
        scored.append(row)
        content_type = str(item.get("content_type", "Post")).title()
        if content_type not in CONTENT_TYPES:
            content_type = "Post"
        format_scores[content_type].append(metrics["score"])

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    winners = ranked[:3]
    averages = {k: round(sum(v) / len(v), 2) for k, v in format_scores.items() if v}
    best_format = max(averages, key=averages.get) if averages else "Post"

    if not items:
        strategy = "Collect performance data from at least 5 posts before making major strategy changes."
    elif winners and winners[0]["score"] >= 60:
        strategy = f"Scale {best_format} content and reuse the strongest hook, topic angle, and CTA from the top-performing posts."
    else:
        strategy = "Run small A/B-style tests on hooks, formats, and CTAs before scaling a content pattern."

    return {
        "posts_analyzed": len(items),
        "best_format": best_format,
        "format_scores": averages,
        "top_posts": winners,
        "strategy": strategy,
        "next_tests": [
            "Test a stronger first-line hook.",
            "Compare a direct CTA with a save/share CTA.",
            "Repeat the strongest topic in a different format.",
        ],
    }
