from app.services.growth import growth_insights, score_content


def test_score_content():
    result = score_content({"reach": 1000, "likes": 50, "comments": 10, "shares": 20, "saves": 20, "clicks": 10})
    assert result["engagements"] == 100
    assert result["engagement_rate"] == 10.0
    assert result["share_save_rate"] == 4.0


def test_growth_insights_selects_winner():
    result = growth_insights(items=[
        {"content_type": "Reel", "title": "A", "reach": 1000, "likes": 60, "shares": 20, "saves": 20},
        {"content_type": "Post", "title": "B", "reach": 1000, "likes": 10, "shares": 2, "saves": 3},
    ])
    assert result["posts_analyzed"] == 2
    assert result["best_format"] == "Reel"
    assert result["top_posts"][0]["title"] == "A"


def test_growth_insights_empty():
    result = growth_insights(items=[])
    assert result["posts_analyzed"] == 0
    assert result["best_format"] == "Post"
