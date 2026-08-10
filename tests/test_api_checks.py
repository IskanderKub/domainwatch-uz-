# Integration tests for the /api/v1/domains/{id}/checks endpoints.
# CheckerService.check_domain itself is unit-tested separately (test_checker_service.py),
# so here it's mocked out - these tests only verify the HTTP wiring (status codes, 404s).
from datetime import datetime, timezone

from app.models.sql_models import CheckResult
from app.services.checker_service import CheckerService


def test_trigger_check_missing_domain_returns_404(client):
    response = client.post("/api/v1/domains/999/checks")
    assert response.status_code == 404


def test_trigger_check_returns_result(client, mocker):
    created = client.post(
        "/api/v1/domains", json={"name": "example.uz", "url": "https://example.uz"}
    ).json()

    # a plain (unsaved) CheckResult is enough - the response only needs its attributes
    fake_result = CheckResult(
        id=1,
        domain_id=created["id"],
        checked_at=datetime.now(timezone.utc),
        is_available=True,
        status_code=200,
        response_time_ms=123.4,
        similarity_ratio=0.99,
        is_suspected_defacement=False,
    )
    mocker.patch.object(CheckerService, "check_domain", return_value=fake_result)

    response = client.post(f"/api/v1/domains/{created['id']}/checks")

    assert response.status_code == 201
    body = response.json()
    assert body["is_available"] is True
    assert body["status_code"] == 200


def test_list_checks_for_missing_domain_returns_404(client):
    response = client.get("/api/v1/domains/999/checks")
    assert response.status_code == 404
