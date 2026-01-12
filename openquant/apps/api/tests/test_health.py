import pytest


@pytest.mark.anyio
async def test_root_health(api_client):
    resp = await api_client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["service"] == "OpenQuant API"


@pytest.mark.anyio
async def test_detailed_health(api_client):
    resp = await api_client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert body["services"]["api"] == "running"

