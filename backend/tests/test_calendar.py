from datetime import date

from app.services.calendar import generate_calendar


def test_seven_day_calendar_shape():
    result = generate_calendar(
        business_name="Bean & Brew", business_type="Cafe", product_name="Cold Coffee",
        offer="Buy 1 Get 1", days=7, start_date="2026-09-15", frequency=4,
    )
    assert result["period_days"] == 7
    assert result["frequency_per_week"] == 4
    assert result["calendar"]
    assert all(item["date"] >= "2026-09-15" for item in result["calendar"])
    assert all(item["content_type"] in {"Reel", "Carousel", "Post", "Story"} for item in result["calendar"])


def test_thirty_day_calendar_has_planned_items():
    result = generate_calendar(
        business_name="Salon One", business_type="Salon", product_name="Hair Spa",
        days=30, start_date=date(2026, 9, 15).isoformat(), frequency=3,
    )
    assert result["period_days"] == 30
    assert len(result["calendar"]) >= 12
    assert all(item["status"] == "Planned" for item in result["calendar"])
