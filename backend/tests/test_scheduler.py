from app.services.scheduler import create_job, retry_job


def test_create_job_defaults_to_queued():
    job = create_job(provider="YouTube", account_name="Demo", content={"title": "Hello"})
    assert job["status"] == "queued"
    assert job["attempts"] == 0
    assert job["provider"] == "YouTube"


def test_retry_job_stops_after_three_attempts():
    job = {"job_id": "x", "attempts": 2, "status": "retrying"}
    failed = retry_job(job, error="temporary failure")
    assert failed["attempts"] == 3
    assert failed["status"] == "failed"
    assert failed["last_error"] == "temporary failure"
