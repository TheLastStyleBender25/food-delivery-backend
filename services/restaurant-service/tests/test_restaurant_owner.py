

def test_create_restaurant(client, owner_user):
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

    response = client.post(
        "/restaurants/create",
        json=payload
    )

    assert response.status_code == 200


def test_customer_cannot_create_restaurant(client, owner_customer):
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

    response = client.post(
        "/restaurants/create",
        json=payload
    )

    assert response.status_code == 403


def test_create_restaurant_without_name(client, owner_user):
    payload = {
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

    response = client.post(
        "/restaurants/create",
        json=payload
    )

    assert response.status_code == 422