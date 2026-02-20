from __future__ import annotations

import pytest
from app.main import API_PREFIX

def test_create_and_get_user(client):
    payload = {
        "username": "alex_01",
        "email": "alex_01@example.com",
        "first_name": "Alex",
        "last_name": "One",
        "role": "user",
        "active": True,
    }
    r = client.post(f"{API_PREFIX}/users", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["username"] == "alex_01"
    user_id = data["id"]

    r2 = client.get(f"{API_PREFIX}/users/{user_id}")
    assert r2.status_code == 200
    assert r2.json()["email"] == "alex_01@example.com"

def test_list_users_filters(client):
    # create two
    client.post(f"{API_PREFIX}/users", json={"username":"u1_test","email":"u1_test@example.com","role":"user","active":True})
    client.post(f"{API_PREFIX}/users", json={"username":"u2_test","email":"u2_test@example.com","role":"guest","active":False})

    r = client.get(f"{API_PREFIX}/users")
    assert r.status_code == 200
    assert len(r.json()) == 2

    r = client.get(f"{API_PREFIX}/users?active=true")
    assert r.status_code == 200
    assert all(u["active"] is True for u in r.json())

    r = client.get(f"{API_PREFIX}/users?active=false")
    assert r.status_code == 200
    assert all(u["active"] is False for u in r.json())

def test_unique_username_email(client):
    base = {"username":"uniq_user","email":"uniq_user@example.com","role":"user","active":True}
    r1 = client.post(f"{API_PREFIX}/users", json=base)
    assert r1.status_code == 201

    # duplicate username
    r2 = client.post(f"{API_PREFIX}/users", json={"username":"uniq_user","email":"other@example.com","role":"user","active":True})
    assert r2.status_code == 409

    # duplicate email
    r3 = client.post(f"{API_PREFIX}/users", json={"username":"other_user","email":"uniq_user@example.com","role":"user","active":True})
    assert r3.status_code == 409

def test_update_user_and_soft_delete(client):
    r = client.post(f"{API_PREFIX}/users", json={"username":"upd_user","email":"upd_user@example.com","role":"user","active":True})
    user_id = r.json()["id"]

    r2 = client.put(f"{API_PREFIX}/users/{user_id}", json={"role":"admin","active":False})
    assert r2.status_code == 200
    assert r2.json()["role"] == "admin"
    assert r2.json()["active"] is False

    r3 = client.delete(f"{API_PREFIX}/users/{user_id}")
    assert r3.status_code == 204

    r4 = client.get(f"{API_PREFIX}/users/{user_id}")
    assert r4.status_code == 200
    assert r4.json()["active"] is False

def test_validation_errors(client):
    # short username
    r = client.post(f"{API_PREFIX}/users", json={"username":"ab","email":"ab@example.com","role":"user","active":True})
    assert r.status_code == 422

    # invalid email
    r = client.post(f"{API_PREFIX}/users", json={"username":"valid_name","email":"not-an-email","role":"user","active":True})
    assert r.status_code == 422
