from app.services.connections import SUPPORTED_PROVIDERS, _fingerprint, publish_dry_run
from app.services.publisher import publish, validate_payload


def test_provider_list_and_fingerprint():
    assert "Instagram" in SUPPORTED_PROVIDERS
    assert _fingerprint("secret") == _fingerprint("secret")
    assert _fingerprint("secret") != _fingerprint("other")


def test_dry_run_never_publishes():
    result = publish_dry_run(provider="Instagram", account_name="demo", content={"caption": "hello"})
    assert result["mode"] == "dry_run"
    assert result["status"] == "ready"
    assert "No social-platform request was sent" in result["message"]


def test_publisher_rejects_live_mode_until_adapter_exists():
    validate_payload(provider="LinkedIn", content={"caption": "hello"})
    try:
        publish(provider="LinkedIn", account_name="demo", content={"caption": "hello"}, dry_run=False)
    except RuntimeError as exc:
        assert "Live publishing adapter is not configured" in str(exc)
    else:
        raise AssertionError("live publishing should not be enabled in V8")
