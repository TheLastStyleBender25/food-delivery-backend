from app.models import User


def test_login_success(client, db):
    register_payload = {
        "name": "Test User",
        "email": "login@example.com",
        "password": "Password123",
        "role": "CUSTOMER"
    }

    client.post(
        "/auth/register",
        json=register_payload
    )

    db_user = db.query(User).filter(User.email == "login@example.com").first()
    db_user.is_verified = True
    db.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_user_not_verified(client):
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "wrongpass@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrongpass@example.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 403

def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "missing@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 404