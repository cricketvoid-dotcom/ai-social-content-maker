import io

import pytest
from PIL import Image

from app.services.creative import create_marketing_image


def sample_jpeg() -> bytes:
    image = Image.new("RGB", (80, 80), "white")
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()


@pytest.mark.asyncio
async def test_creative_image_falls_back_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = await create_marketing_image(image_bytes=sample_jpeg(), prompt="clean product photo")
    assert result["status"] == "original"
    assert result["image_data"].startswith("data:image/jpeg;base64,")


def test_creative_rejects_invalid_image():
    import asyncio
    with pytest.raises(ValueError):
        asyncio.run(create_marketing_image(image_bytes=b"not-an-image", prompt="test"))
