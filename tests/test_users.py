def test_healthz(client):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_crud_user(client):
    # Create
    r = client.post("/users", json={
        "username": "alex",
        "email": "alex@test.com",
        "first_name": "Alex",
        "last_name": "Dev",
        "role": "admin",
        "active": True
    })
    assert r.status_code == 201, r.text
    body = r.json()
    user_id = body["id"]
    assert body["username"] == "alex"
    assert body["email"] == "alex@test.com"

    # Get
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200
    assert r.json()["id"] == user_id

    # List
    r = client.get("/users")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Update
    r = client.put(f"/users/{user_id}", json={"role": "user", "active": False})
    assert r.status_code == 200, r.text
    assert r.json()["role"] == "user"
    assert r.json()["active"] is False

    # Delete
    r = client.delete(f"/users/{user_id}")
    assert r.status_code == 204

    # Get deleted
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 404

def test_unique_constraints(client):
    r1 = client.post("/users", json={"username": "u1", "email": "u1@test.com", "role": "user"})
    assert r1.status_code == 201

    r2 = client.post("/users", json={"username": "u1", "email": "u2@test.com", "role": "user"})
    assert r2.status_code == 409

    r3 = client.post("/users", json={"username": "u3", "email": "u1@test.com", "role": "user"})
    assert r3.status_code == 409
