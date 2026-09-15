from app.services.optimizer import optimize_content

def test_optimizer_strong():
    r=optimize_content(content_type="Reel",title="Coffee",metrics={"engagement_rate":10,"shares":2,"saves":2})
    assert r["strategy"]=="Scale this format"
    assert r["recommended_length"]=="15–25 seconds"

def test_optimizer_weak():
    r=optimize_content(content_type="Carousel",title="Offer",metrics={"engagement_rate":1})
    assert r["strategy"]=="Rework before repeating"
    assert r["recommended_length"]=="5–7 slides"
