import asyncio
import os

from app.services.content import generate_content


def test_local_generation_without_api_key():
    old_key = os.environ.pop("OPENAI_API_KEY", None)
    try:
        result = asyncio.run(generate_content(
            business_type="Cafe",
            business_name="Bean & Brew",
            product_name="Cold Coffee",
            offer="Buy 1 Get 1",
            price="₹149",
            location="Connaught Place",
            phone="98765 43210",
            additional_info="Available all day",
            has_photo=True,
        ))
        assert result["headline"] == "Buy 1 Get 1"
        assert len(result["hashtags"]) == 5
        assert result["design"]["has_photo"] is True
    finally:
        if old_key is not None:
            os.environ["OPENAI_API_KEY"] = old_key
