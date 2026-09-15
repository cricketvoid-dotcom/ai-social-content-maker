from app.services.automation import calculate_analytics, make_schedule_item, performance_recommendation

def test_analytics_rates():
    result=calculate_analytics(impressions=1000,reach=800,likes=40,comments=8,shares=12,saves=20,clicks=16)
    assert result["engagements"]==80
    assert result["engagement_rate"]==10.0
    assert result["click_rate"]==2.0

def test_schedule_item():
    result=make_schedule_item(calendar_item={"date":"2026-09-15","content_type":"Reel","title":"Demo","concept":"Show it"},scheduled_at="2026-09-15T18:00:00")
    assert result["status"]=="Scheduled"
    assert result["scheduled_at"]=="2026-09-15T18:00:00"

def test_recommendation():
    assert performance_recommendation(metrics={"engagement_rate":10,"shares":2,"saves":2})["signal"]=="strong"
    assert performance_recommendation(metrics={"engagement_rate":1,"shares":0,"saves":0})["signal"]=="needs_testing"
