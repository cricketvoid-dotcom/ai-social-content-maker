from app.services.platforms import generate_platform_content


def test_generates_selected_platforms():
    result = generate_platform_content(
        business_name="Demo Cafe",
        topic="New weekend offer",
        base_caption="Fresh coffee and snacks this weekend.",
        platforms=["Instagram", "LinkedIn", "X"],
    )
    assert set(result["platforms"]) == {"Instagram", "LinkedIn", "X"}
    assert result["platforms"]["Instagram"]["format"] == "Post or Reel"
    assert len(result["platforms"]["X"]["text"]) <= 280


def test_unknown_platform_is_ignored():
    result = generate_platform_content(
        business_name="Demo",
        topic="Offer",
        platforms=["Unknown", "Facebook"],
    )
    assert set(result["platforms"]) == {"Facebook"}
