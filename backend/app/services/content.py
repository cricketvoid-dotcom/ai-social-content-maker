import json
import os
from typing import Any


def _local_content(*, business_type: str, business_name: str, product_name: str,
                   offer: str, price: str, location: str, phone: str,
                   additional_info: str, has_photo: bool) -> dict[str, Any]:
    brand = business_name.strip() or business_type.strip().title()
    product = product_name.strip()
    headline = offer.strip() or f"Discover {product}"
    subheadline = f"Fresh picks from {brand}"
    caption = (
        f"✨ {headline}! {product} is ready for you at {brand}. "
        f"{additional_info.strip()} "
        f"{('📍 ' + location.strip() + ' ' if location.strip() else '')}"
        f"{('📞 ' + phone.strip() if phone.strip() else '')}"
    ).strip()
    tags = [
        f"#{business_type.strip().replace(' ', '')}",
        f"#{product.replace(' ', '')}",
        "#LocalBusiness", "#ShopLocal", "#InstagramMarketing",
    ]
    return {
        "headline": headline, "subheadline": subheadline, "caption": caption,
        "hashtags": tags,
        "cta": "DM us to order" if not phone.strip() else f"Call {phone.strip()} today",
        "design": {"brand": brand, "price": price.strip(), "location": location.strip(),
                   "phone": phone.strip(), "has_photo": has_photo},
    }


def _local_v2(*, business_type: str, business_name: str, product_name: str,
              offer: str, price: str, location: str, phone: str,
              additional_info: str, **_: Any) -> dict[str, Any]:
    brand = business_name.strip() or business_type.strip().title()
    product = product_name.strip()
    hook = offer.strip() or f"You need to try {product}"
    return {
        "reel_ideas": [
            {"title": "Problem → Solution", "hook": f"Still looking for {product}?", "script": [
                "Show the problem in the first 2 seconds.", f"Reveal {product} with a quick close-up.",
                f"Show the result/benefit and finish with: {hook}.",
            ], "duration": "10–15 sec"},
            {"title": "3 Reasons to Try It", "hook": f"3 reasons {product} is worth trying 👀", "script": [
                f"Reason 1: Show {product}.", f"Reason 2: Highlight {offer or 'the key benefit'}.",
                f"Reason 3: Show the final result and invite viewers to contact {brand}.",
            ], "duration": "15–20 sec"},
            {"title": "Behind the Scenes", "hook": f"How we make {product} ✨", "script": [
                "Show a fast behind-the-scenes clip.", "Cut through 3–4 satisfying process shots.",
                f"End on the finished {product} with a clear CTA.",
            ], "duration": "12–18 sec"},
        ],
        "carousel_ideas": [
            {"title": f"Why {product}?", "slides": ["Hook", "What it is", "Top benefits", "Offer / price", "CTA"]},
            {"title": "Before You Buy", "slides": ["Common problem", "What to look for", "Why this product", "Proof / result", "How to order"]},
        ],
        "posting_suggestion": {
            "best_days": ["Tuesday", "Thursday", "Saturday"],
            "best_time": "6:00 PM–8:00 PM local time",
            "frequency": "3–4 posts/reels per week",
            "tip": "Test these slots for 2 weeks, then keep the times that produce the strongest saves, shares, and comments.",
        },
    }


async def generate_content(*, include_v2: bool = False, **kwargs: Any) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    base = _local_content(**kwargs)
    v2 = _local_v2(**kwargs) if include_v2 else {}
    if not api_key:
        return {**base, **v2}

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    task = """Create Instagram content for a local business. Return ONLY valid JSON.
Keys: headline, subheadline, caption, hashtags, cta, reel_ideas, carousel_ideas, posting_suggestion.
hashtags: array of 5 strings.
reel_ideas: array of 3 objects with title, hook, script (array), duration.
carousel_ideas: array of 2 objects with title and slides (array).
posting_suggestion: object with best_days (array), best_time, frequency, tip.
Business type: {business_type}
Business name: {business_name}
Product/service: {product_name}
Offer: {offer}
Price: {price}
Location: {location}
Phone: {phone}
Extra info: {additional_info}
""".format(**kwargs)
    try:
        response = await client.chat.completions.create(
            model=model, temperature=0.8, response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are an expert local-business social media strategist."},
                {"role": "user", "content": task},
            ],
        )
        data = json.loads(response.choices[0].message.content or "{}")
        return {**base, **v2, **data}
    except Exception:
        # Keep the product usable even if an AI provider is temporarily unavailable.
        return {**base, **v2}
