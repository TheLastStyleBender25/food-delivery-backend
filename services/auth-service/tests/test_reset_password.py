from app.core.redis_com import redis_client
from app.models import User
from app.core.redis_otp import save_otp, get_otp, delete_otp


def test_reset_password_success(client, db):

    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "reset@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )
    user = db.query(User).filter(User.name == "Test User").first()
    user.is_verified = True
    db.commit()

    # Request password reset
    forgot_response = client.post(
        "/auth/forgot-password",
        json={
            "email": "reset@example.com"
        }
    )

    assert forgot_response.status_code == 200

    # Fetch OTP from Redis (simulates user reading email)
    otp = get_otp("reset@example.com")

    response = client.post(
        "/auth/reset-password",
        json={
            "email": "reset@example.com",
            "otp": otp,
            "new_password": "NewPassword456"
        }
    )

    assert response.status_code == 200


def test_reset_password_wrong_otp(client, db):
    # Register user
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "wrongotp@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )

    user = db.query(User).filter(User.name == "Test User").first()
    user.is_verified = True
    db.commit()

    # Generate and store OTP in Redis
    forgot_response = client.post(
        "/auth/forgot-password",
        json={
            "email": "wrongotp@example.com"
        }
    )

    assert forgot_response.status_code == 200

    # Use incorrect OTP
    response = client.post(
        "/auth/reset-password",
        json={
            "email": "wrongotp@example.com",
            "otp": "999999",
            "new_password": "NewPassword123"
        }
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Incorrect OTP"