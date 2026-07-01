from app.models import User
from app.core.jwt import create_email_verification_token, create_access_token


def test_verify_email_success(client, db):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "verify@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )

    user = db.query(User).filter(
        User.email == "verify@example.com"
    ).first()

    # Generate verification token
    token = create_email_verification_token(
        str(user.id)
    )

    response = client.get(
        f"/auth/verify-email?token={token}"
    )

    assert response.status_code == 200

    db.refresh(user)

    assert user.is_verified is True

def test_verify_email_invalid_token(client):
    response = client.get(
        "/auth/verify-email?token=invalid_token"
    )

    assert response.status_code == 401



def test_verify_email_user_not_found(client):
    fake_user_id = "00000000-0000-0000-0000-000000000000"

    token = create_email_verification_token(
        fake_user_id
    )

    response = client.get(
        f"/auth/verify-email?token={token}"
    )

    assert response.status_code == 404

def test_verify_email_already_verified(client, db):
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "verified@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )

    user = db.query(User).filter(
        User.email == "verified@example.com"
    ).first()

    token = create_email_verification_token(
        str(user.id)
    )

    client.get(
        f"/auth/verify-email?token={token}"
    )

    response = client.get(
        f"/auth/verify-email?token={token}"
    )

    assert response.status_code == 200