from app.services.content import _local_content, _local_v2


def sample():
    return dict(
        business_type="Cafe", business_name="Bean & Brew", product_name="Cold Coffee",
        offer="Buy 1 Get 1", price="₹149", location="Delhi", phone="9876543210",
        additional_info="Dine-in and takeaway", has_photo=True,
    )


def test_v1_content_shape():
    result = _local_content(**sample())
    assert result["headline"] == "Buy 1 Get 1"
    assert len(result["hashtags"]) == 5
    assert result["design"]["has_photo"] is True


def test_v2_content_shape():
    result = _local_v2(**sample())
    assert len(result["reel_ideas"]) == 3
    assert all(r["hook"] and r["script"] for r in result["reel_ideas"])
    assert len(result["carousel_ideas"]) == 2
    assert result["posting_suggestion"]["best_days"]
