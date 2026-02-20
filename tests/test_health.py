from __future__ import annotations

from app.main import API_PREFIX

def test_live(client):
    r = client.get(f"{API_PREFIX}/health/live")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert "X-Request-Id" in r.headers

def test_ready(client):
    r = client.get(f"{API_PREFIX}/health/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
