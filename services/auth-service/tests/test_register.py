def test_register_success(client):
    response = client.post("/auth/register",json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        })
    assert response.status_code == 200
    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["role"] == "CUSTOMER"

def test_dupliacte_email(client):
    payload = {"name": "Test1",
            "email": "test1@example.com",
            "password": "Password123",
            "role": "CUSTOMER"}
    response1 = client.post("/auth/register",json= payload)
    response2 = client.post("/auth/register",json= payload)

    assert response1.status_code == 200
    assert response2.status_code == 400


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "invalid-email",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )

    assert response.status_code == 422

def test_register_weak_password(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "123",
            "role": "CUSTOMER"
        }
    )

    assert response.status_code == 422
