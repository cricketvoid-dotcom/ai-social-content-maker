import json
import os
from typing import Any

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _brand_design(kwargs: dict[str, Any]) -> dict[str, Any]:
    return {
        "brand": kwargs.get("business_name", "").strip() or kwargs.get("business_type", "").strip().title(),
        "price": kwargs.get("price", "").strip(), "location": kwargs.get("location", "").strip(),
        "phone": kwargs.get("phone", "").strip(), "has_photo": kwargs.get("has_photo", False),
        "tagline": kwargs.get("brand_tagline", "").strip(),
        "primary_color": kwargs.get("brand_primary_color", "#171722"),
        "secondary_color": kwargs.get("brand_secondary_color", "#ffffff"),
        "accent_color": kwargs.get("brand_accent_color", "#5146d8"),
        "font_family": kwargs.get("brand_font_family", "Inter"),
        "social_handle": kwargs.get("brand_social_handle", "").strip(),
        "logo_data": kwargs.get("brand_logo", ""),
    }


def _reel_schedule(reels_per_week: int, max_reels_per_day: int) -> list[dict[str, Any]]:
    count = max(1, min(int(reels_per_week or 1), 21))
    per_day = max(1, min(int(max_reels_per_day or 1), 3))
    schedule: list[dict[str, Any]] = []
    index = 0
    for day in WEEK_DAYS:
        for slot in range(per_day):
            if index >= count:
                break
            schedule.append({"reel_number": index + 1, "day": day, "slot": slot + 1})
            index += 1
        if index >= count:
            break
    return schedule


def _simple_reels(*, business_type: str, business_name: str, product_name: str,
                  offer: str, reels_per_week: int, max_reels_per_day: int) -> list[dict[str, Any]]:
    product = product_name.strip() or "your product/service"
    brand = business_name.strip() or business_type.strip().title() or "your business"
    schedule = _reel_schedule(reels_per_week, max_reels_per_day)
    styles = [
        ("Educational", f"3 things to know about {product}"),
        ("Problem → Solution", f"Having trouble with {product}? Try this."),
        ("Product/Service", f"See what makes {product} useful."),
        ("Storytelling", f"A quick story about {product} at {brand}."),
        ("Promotional", f"Here's why you should check out {product}."),
        ("FAQ", f"One common question about {product}, answered."),
        ("Behind the Scenes", f"See a quick look behind {brand}."),
    ]
    reels = []
    for i, item in enumerate(schedule):
        style, idea = styles[i % len(styles)]
        offer_text = offer.strip() or "the key benefit"
        reels.append({
            "number": item["reel_number"], "day": item["day"], "slot": item["slot"],
            "title": idea, "type": style,
            "hook": f"Want to know more about {product}? Here's what you should know.",
            "scene_by_scene": [
                "Show the topic/product and say the hook.",
                f"Show {product} and explain the main point.",
                f"Show the benefit or result: {offer_text}.",
                "Finish with the CTA on screen."
            ],
            "script": f"Want to know more about {product}? Here's what you should know. Show the product, explain the main benefit, then finish with a clear call to action.",
            "cta": f"Follow {brand} for more and DM us to know more.",
            "caption": f"Thinking about {product}? Here's a quick tip to help you out. Save this Reel and share it with someone who needs it!",
            "hashtags": [f"#{business_type.strip().replace(' ', '')}", f"#{product.replace(' ', '')}", "#Reels", "#SmallBusiness", "#Tips"],
            "duration": "15–30 sec",
        })
    return reels


def _local_content(*, business_type: str, business_name: str, product_name: str,
                   offer: str, price: str, location: str, phone: str,
                   additional_info: str, has_photo: bool, **kwargs: Any) -> dict[str, Any]:
    brand = business_name.strip() or business_type.strip().title()
    product = product_name.strip()
    headline = offer.strip() or f"Discover {product}"
    tagline = kwargs.get("brand_tagline", "").strip()
    subheadline = tagline or f"Fresh picks from {brand}"
    caption = (
        f"✨ {headline}! {product} is ready for you at {brand}. "
        f"{additional_info.strip()} "
        f"{('📍 ' + location.strip() + ' ' if location.strip() else '')}"
        f"{('📞 ' + phone.strip() if phone.strip() else '')}"
    ).strip()
    tags = [f"#{business_type.strip().replace(' ', '')}", f"#{product.replace(' ', '')}", "#LocalBusiness", "#ShopLocal", "#InstagramMarketing"]
    reels_per_week = kwargs.get("reels_per_week", 3)
    max_reels_per_day = kwargs.get("max_reels_per_day", 1)
    return {
        "headline": headline, "subheadline": subheadline, "caption": caption, "hashtags": tags,
        "cta": "DM us to order" if not phone.strip() else f"Call {phone.strip()} today",
        "design": _brand_design({**kwargs, "business_name": business_name, "business_type": business_type, "product_name": product_name, "price": price, "location": location, "phone": phone, "has_photo": has_photo}),
        "reel_ideas": _simple_reels(business_type=business_type, business_name=business_name, product_name=product_name, offer=offer, reels_per_week=reels_per_week, max_reels_per_day=max_reels_per_day),
    }


def _local_v2(*, business_type: str, business_name: str, product_name: str,
              offer: str, price: str, location: str, phone: str,
              additional_info: str, **kwargs: Any) -> dict[str, Any]:
    product = product_name.strip()
    return {
        "reel_ideas": _simple_reels(
            business_type=business_type, business_name=business_name, product_name=product,
            offer=offer, reels_per_week=kwargs.get("reels_per_week", 3),
            max_reels_per_day=kwargs.get("max_reels_per_day", 1),
        ),
        "carousel_ideas": [{"title": f"Why {product}?", "slides": ["Hook", "What it is", "Top benefits", "Offer / price", "CTA"]}, {"title": "Before You Buy", "slides": ["Common problem", "What to look for", "Why this product", "Proof / result", "How to order"]}],
        "posting_suggestion": {"best_days": ["Tuesday", "Thursday", "Saturday"], "best_time": "6:00 PM–8:00 PM local time", "frequency": f"{kwargs.get('reels_per_week', 3)} reels per week", "tip": "Use the generated Reel schedule, then adjust posting times after you collect performance data."},
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
    reels_per_week = max(1, min(int(kwargs.get("reels_per_week", 3)), 21))
    max_reels_per_day = max(1, min(int(kwargs.get("max_reels_per_day", 1)), 3))
    task = """Create Instagram content for a local business. Return ONLY valid JSON.
Keys: headline, subheadline, caption, hashtags, cta, reel_ideas, carousel_ideas, posting_suggestion.
hashtags: array of 5 strings.
reel_ideas MUST contain exactly {reels_per_week} objects. Each object MUST have: number, day, slot, title, type, hook, scene_by_scene, script, cta, caption, hashtags, duration.
Keep every Reel simple and ready to shoot. scene_by_scene must be a short array of 3-5 simple actions. script must be a short natural voiceover, not a long screenplay. cta, caption and hashtags must be specific to that Reel.
Schedule exactly {reels_per_week} Reels across the week and never place more than {max_reels_per_day} Reel(s) on one day. Use Monday-Sunday.
carousel_ideas: array of 2 objects with title and slides (array). posting_suggestion: object with best_days, best_time, frequency, tip.
Business type: {business_type}
Business name: {business_name}
Product/service: {product_name}
Offer: {offer}
Price: {price}
Location: {location}
Phone: {phone}
Extra info: {additional_info}
Brand tagline: {brand_tagline}
""".format(reels_per_week=reels_per_week, max_reels_per_day=max_reels_per_day, **kwargs)
    try:
        response = await client.chat.completions.create(model=model, temperature=0.8, response_format={"type": "json_object"}, messages=[
            {"role": "system", "content": "You are an expert local-business social media strategist. Make the output simple for a business owner to shoot and post."},
            {"role": "user", "content": task},
        ])
        data = json.loads(response.choices[0].message.content or "{}")
        merged = {**base, **v2, **data}
        if len(data.get("reel_ideas", [])) != reels_per_week:
            merged["reel_ideas"] = base["reel_ideas"]
        merged["design"] = {**base["design"], **data.get("design", {})}
        return merged
    except Exception:
        return {**base, **v2}
