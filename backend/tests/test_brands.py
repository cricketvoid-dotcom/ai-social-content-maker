def test_brand_crud_is_persistent(monkeypatch, tmp_path):
    from app.services import brands
    monkeypatch.setattr(brands, "DB_PATH", tmp_path / "brands.db")
    created = brands.create_brand({
        "business_name": "Bean & Brew", "business_type": "Cafe", "tagline": "Fresh daily",
        "primary_color": "#111111", "secondary_color": "#ffffff", "accent_color": "#ff9900",
        "font_family": "Inter", "phone": "123", "location": "Delhi", "social_handle": "@beanbrew",
        "logo_data": "data:image/png;base64,abc",
    })
    assert created["id"] == 1
    assert brands.get_brand(1)["tagline"] == "Fresh daily"
    assert len(brands.list_brands()) == 1
    updated = brands.update_brand(1, {"tagline": "Made with care"})
    assert updated["tagline"] == "Made with care"
    assert brands.delete_brand(1) is True
    assert brands.get_brand(1) is None
