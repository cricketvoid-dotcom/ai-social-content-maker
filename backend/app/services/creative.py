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


async def create_marketing_image(
    *,
    image_bytes: bytes,
    prompt: str,
    business_name: str = "",
    product_name: str = "",
) -> dict[str, Any]:
    normalised = _normalise_image(image_bytes)
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _fallback_image(normalised)

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=api_key)
    # GPT-Image-2 is the current OpenAI image model and supports reference-image editing.
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2").strip() or "gpt-image-2"
    context = ", ".join(x for x in [business_name.strip(), product_name.strip()] if x.strip())
    full_prompt = (
        "Upgrade this low-quality ordinary smartphone business photo into a high-quality, realistic,
        professional marketing photograph. "
        "Preserve the actual product identity, shape, quantity, colors, and important visual details of the source photo. "
        "Improve resolution, sharpness, exposure, white balance, lighting, depth, composition, and background cleanliness. "
        "Remove ordinary smartphone noise, blur, compression artifacts, distracting clutter, and poor lighting while keeping the product believable. "
        "Do not replace the product with a different product. Do not invent people, fake logos, fake prices, watermarks, or unrelated objects. "
        "The final image should look like a premium commercial photo of the same real product, not an obviously AI-generated scene. "
        f"Business context: {context or 'local business'}. "
        f"Additional creative direction: {prompt.strip() or 'clean premium natural product photography'}"
    )

    response = await client.images.edit(
        model=model,
        image=[io.BytesIO(normalised)],
        prompt=full_prompt,
        size="1024x1024",
        quality="high",
        input_fidelity="high",
        output_format="png",
    )
    if not response.data:
        raise RuntimeError("The image model returned no image data.")
    b64 = getattr(response.data[0], "b64_json", None)
    if not b64:
        raise RuntimeError("The image model returned no image data.")
    return {
        "status": "generated",
        "message": "Low-quality source photo upgraded into a high-quality marketing image successfully.",
        "image_data": f"data:image/png;base64,{b64}",
        "model": model,
    }
