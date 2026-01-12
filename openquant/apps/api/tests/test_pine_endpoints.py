import pytest


@pytest.mark.anyio
async def test_pine_templates(api_client):
    resp = await api_client.get("/pine/templates")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body.get("templates"), list)
    assert any(t.get("name") == "RSI Strategy" for t in body["templates"])


@pytest.mark.anyio
async def test_pine_generate_validate_fix(api_client):
    gen = await api_client.post(
        "/pine/generate",
        json={"description": "RSI crossover strategy", "script_type": "strategy"},
    )
    assert gen.status_code == 200
    gen_body = gen.json()
    assert gen_body["is_valid"] is True
    assert gen_body["errors"] == []
    assert "//@version=5" in gen_body["code"]
    assert "strategy(" in gen_body["code"]

    validate = await api_client.post("/pine/validate", params={"code": gen_body["code"]})
    assert validate.status_code == 200
    val_body = validate.json()
    assert val_body["is_valid"] is True
    assert val_body["errors"] == []

    fix = await api_client.post(
        "/pine/fix",
        json={"code": "bad code", "error_message": "undeclared identifier"},
    )
    assert fix.status_code == 200
    fix_body = fix.json()
    assert fix_body["is_valid"] is True

