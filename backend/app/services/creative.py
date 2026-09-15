from __future__ import annotations

import base64
import io
import os
from typing import Any

from PIL import Image


MAX_IMAGE_BYTES = 10 * 1024 * 1024


def _normalise_image(data: bytes) -> bytes:
    if not data or len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Image must be between 1 byte and 10 MB.")
    try:
        image = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception as exc:
        raise ValueError("Unsupported or invalid image.") from exc
    image.thumbnail((2048, 2048))
    output = io.BytesIO()
    image.save(output, format="JPEG", quality=92, optimize=True)
    return output.getvalue()


def _fallback_image(data: bytes) -> dict[str, Any]:
    encoded = base64.b64encode(data).decode("ascii")
    return {
        "status": "original",
        "message": "AI image generation is not configured, so the uploaded photo is returned unchanged.",
        "image_data": f"data:image/jpeg;base64,{encoded}",
        "model": None,
    }


async def create_marketing_image(*, image_bytes: bytes, prompt: str, business_name: str = "", product_name: str = "") -> dict[str, Any]:
    normalised = _normalise_image(image_bytes)
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _fallback_image(normalised)

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
    context = ", ".join(x for x in [business_name.strip(), product_name.strip()] if x.strip())
    full_prompt = (
        "Transform this ordinary business photo into a polished, realistic social-media marketing photo. "
        "Preserve the identity and important visual characteristics of the actual product or subject. "
        "Improve lighting, clarity, composition and background while keeping the result believable and commercially useful. "
        "Do not add people, fake logos, fake prices, watermarks, or unrelated products. "
        f"Business context: {context or 'local business'}. "
        f"Additional creative direction: {prompt.strip() or 'clean premium natural product photography'}"
    )

    response = await client.images.edit(
        model=model,
        image=normalised,
        prompt=full_prompt,
        size="1024x1024",
        quality="medium",
    )
    b64 = getattr(response.data[0], "b64_json", None)
    if not b64:
        raise RuntimeError("The image model returned no image data.")
    return {
        "status": "generated",
        "message": "AI marketing image generated successfully.",
        "image_data": f"data:image/png;base64,{b64}",
        "model": model,
    }
