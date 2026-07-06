from app.main import app
from app.dependencies.auth import get_current_user
from app.schemas.token_payload import TokenPayload

def test_get_nearby_restaurants(client):
    def owner_override():
        return TokenPayload(sub="22222222-2222-2222-2222-222222222222", role="RESTAURANT_OWNER")

    app.dependency_overrides[get_current_user] = owner_override

    # Create restaurant as owner
    payload = {
        "name": "Pizza Palace",
        "description": "Italian food",
        "phone": "9876543210",
        "address": "Connaught Place",
        "city": "Delhi",
        "state": "Delhi",
        "latitude": 28.6200,
        "longitude": 77.2150,
        "delivery_radius_km": 5,
        "minimum_order_amount": 200,
        "average_preparation_time_minutes": 20,
        "opens_at": "10:00:00",
        "closes_at": "23:00:00"
    }

    create_response = client.post(
        "/restaurants/create",
        json=payload
    )

    assert create_response.status_code == 200

    def customer_override():
        return TokenPayload(sub="33333333-3333-3333-3333-333333333333", role="CUSTOMER")

    app.dependency_overrides[get_current_user] = customer_override
    # Switch to customer authentication
    response = client.get(
        "/restaurants/get_nearby_restaurants",
        params={
            "latitude": 28.6139,
            "longitude": 77.2090,
            "page": 1,
            "size": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0


def test_get_nearby_restaurants_empty(client):

    def owner_override():
        return TokenPayload(
            sub="11111111-1111-1111-1111-111111111111",
            role="RESTAURANT_OWNER"
        )

    app.dependency_overrides[get_current_user] = owner_override

    payload = {
        "name": "Far Away Restaurant",
        "description": "Italian food",
        "phone": "9876543210",
        "address": "Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "delivery_radius_km": 5,
        "minimum_order_amount": 200,
        "average_preparation_time_minutes": 20,
        "opens_at": "10:00:00",
        "closes_at": "23:00:00"
    }

    client.post(
        "/restaurants/create",
        json=payload
    )

    def customer_override():
        return TokenPayload(
            sub="22222222-2222-2222-2222-222222222222",
            role="CUSTOMER"
        )

    app.dependency_overrides[get_current_user] = customer_override

    response = client.get(
        "/restaurants/get_nearby_restaurants",
        params={
            "latitude": 28.6139,
            "longitude": 77.2090,
            "page": 1,
            "size": 10
        }
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_filter_by_preparation_time(client):

    def owner_override():
        return TokenPayload(
            sub="11111111-1111-1111-1111-111111111111",
            role="RESTAURANT_OWNER"
        )

    app.dependency_overrides[get_current_user] = owner_override

    payload = {
        "name": "Slow Restaurant",
        "description": "Italian food",
        "phone": "9876543210",
        "address": "Delhi",
        "city": "Delhi",
        "state": "Delhi",
        "latitude": 28.6200,
        "longitude": 77.2150,
        "delivery_radius_km": 5,
        "minimum_order_amount": 200,
        "average_preparation_time_minutes": 45,
        "opens_at": "10:00:00",
        "closes_at": "23:00:00"
    }

    client.post(
        "/restaurants/create",
        json=payload
    )

    def customer_override():
        return TokenPayload(
            sub="22222222-2222-2222-2222-222222222222",
            role="CUSTOMER"
        )

    app.dependency_overrides[get_current_user] = customer_override

    response = client.get(
        "/restaurants/get_nearby_restaurants",
        params={
            "latitude": 28.6139,
            "longitude": 77.2090,
            "page": 1,
            "size": 10,
            "max_preparation_time": 20
        }
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()) == 0
