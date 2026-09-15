import json
import os
from typing import Any


def _local_content(*, business_type: str, business_name: str, product_name: str,
                   offer: str, price: str, location: str, phone: str,
                   additional_info: str, has_photo: bool) -> dict[str, Any]:
    brand = business_name.strip() or business_type.strip().title()
    headline = offer.strip() or f"Discover {product_name.strip()}"
    subheadline = f"Fresh picks from {brand}" if brand else f"Made for you"
    caption = (
        f"✨ {headline}! {product_name.strip()} is ready for you at {brand}. "
        f"{additional_info.strip()} "
        f"{('📍 ' + location.strip() + ' ' if location.strip() else '')}"
        f"{('📞 ' + phone.strip() if phone.strip() else '')}"
    ).strip()
    tags = [
        f"#{business_type.strip().replace(' ', '')}",
        f"#{product_name.strip().replace(' ', '')}",
        "#LocalBusiness",
        "#ShopLocal",
        "#InstagramMarketing",
    ]
    return {
        "headline": headline,
        "subheadline": subheadline,
        "caption": caption,
        "hashtags": tags,
        "cta": "DM us to order" if not phone.strip() else f"Call {phone.strip()} today",
        "design": {
            "brand": brand,
            "price": price.strip(),
            "location": location.strip(),
            "phone": phone.strip(),
            "has_photo": has_photo,
        },
    }


async def generate_content(**kwargs: Any) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _local_content(**kwargs)

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    prompt = f"""Create concise Instagram promotional copy for a local business.
Return ONLY valid JSON with keys: headline, subheadline, caption, hashtags, cta.
hashtags must be an array of 5 short hashtags.
Business type: {kwargs['business_type']}
Business name: {kwargs['business_name']}
Product: {kwargs['product_name']}
Offer: {kwargs['offer']}
Price: {kwargs['price']}
Location: {kwargs['location']}
Phone: {kwargs['phone']}
Additional info: {kwargs['additional_info']}
"""
    response = await client.chat.completions.create(
        model=model,
        temperature=0.8,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an expert local-business social media copywriter."},
            {"role": "user", "content": prompt},
        ],
    )
    data = json.loads(response.choices[0].message.content or "{}")
    local = _local_content(**kwargs)
    return {
        **local,
        **data,
        "hashtags": data.get("hashtags") or local["hashtags"],
        "design": local["design"],
    }
