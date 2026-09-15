from __future__ import annotations

from datetime import date, timedelta
from typing import Any


CONTENT_TYPES = ("Reel", "Carousel", "Post", "Story")


def _ideas(product: str, offer: str) -> list[tuple[str, str, str]]:
    offer_text = offer or "your latest offer"
    return [
        ("Reel", f"3 reasons to try {product}", "Hook with a bold benefit, show the product, then finish with a CTA."),
        ("Carousel", f"Why choose {product}?", "Explain the problem, benefits, proof, offer, and CTA slide by slide."),
        ("Post", f"{product} spotlight", "Use a clean product photo with the main benefit and a short CTA."),
        ("Story", "Quick offer reminder", f"Show {product}, mention {offer_text}, and invite a DM or visit."),
        ("Reel", f"Behind the scenes: {product}", "Show 3–4 quick process clips and reveal the finished result."),
        ("Carousel", f"Before you buy {product}", "Cover what to look for, key benefits, proof, price, and how to order."),
        ("Post", "Customer-value post", "Share one useful tip related to the product or service and connect it to the business."),
    ]


def generate_calendar(*, business_name: str, business_type: str, product_name: str,
                      offer: str = "", days: int = 7, start_date: str | None = None,
                      frequency: int = 4, **_: Any) -> dict[str, Any]:
    days = max(7, min(days, 30))
    frequency = max(1, min(frequency, 7))
    try:
        start = date.fromisoformat(start_date) if start_date else date.today()
    except ValueError:
        start = date.today()

    ideas = _ideas(product_name.strip(), offer.strip())
    calendar: list[dict[str, Any]] = []
    publish_index = 0
    for offset in range(days):
        day = start + timedelta(days=offset)
        # Spread the requested number of publishing slots through the week.
        publish = (offset * frequency) % 7 < frequency
        if not publish:
            continue
        content_type, title, concept = ideas[publish_index % len(ideas)]
        calendar.append({
            "date": day.isoformat(),
            "day": day.strftime("%A"),
            "content_type": content_type,
            "title": title,
            "concept": concept,
            "status": "Planned",
        })
        publish_index += 1

    return {
        "business_name": business_name.strip(),
        "business_type": business_type.strip(),
        "period_days": days,
        "frequency_per_week": frequency,
        "calendar": calendar,
    }
