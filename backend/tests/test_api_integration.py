from app.main import app


def test_key_endpoints_are_registered() -> None:
    paths = {route.path for route in app.routes}
    assert "/api/v1/health" in paths
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/auth/me" in paths
    assert "/api/v1/dashboard/summary" in paths
    assert "/api/v1/positions" in paths
    assert "/api/v1/trades" in paths
    assert "/api/v1/strategies" in paths
    assert "/api/v1/risk/summary" in paths
    assert "/api/v1/margin/summary" in paths
    assert "/api/v1/performance/summary" in paths
    assert "/api/v1/income" in paths
    assert "/api/v1/imports" in paths
    assert "/api/v1/audit-log" in paths

    assert "/api/v1/imports/intake" in paths
    assert "/api/v1/imports/{import_batch_id}" in paths
    assert "/api/v1/imports/{import_batch_id}/parse" in paths
