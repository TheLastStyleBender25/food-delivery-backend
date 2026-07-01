from app.models import User


def test_forgot_password_success(client, db):
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "forgot@example.com",
            "password": "Password123",
            "role": "CUSTOMER"
        }
    )
    user = db.query(User).filter(User.email == "forgot@example.com").first()
    user.is_verified = True
    db.commit()

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": "forgot@example.com"
        }
    )

    assert response.status_code == 200