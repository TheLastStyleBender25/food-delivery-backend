import uuid
from sqlalchemy import select
from app.models import MenuItem
from app.schemas.internal import RestaurantResponse


async def test_create_menu_item(client, owner_user, monkeypatch):
    restaurant_id = uuid.uuid4()

    async def mock_get_restaurant(self, restaurant_id):
        return RestaurantResponse(
            id=restaurant_id,
            owner_id="22222222-2222-2222-2222-222222222222",
            status="OPEN",
        )

    monkeypatch.setattr(
        "app.clients.restaurant_client.RestaurantClient.get_restaurant",
        mock_get_restaurant,
    )

    response = await client.post(
        f"/owner/restaurants/{restaurant_id}/menu-items",
        json={
            "name": "Pizza",
            "description": "Cheese Pizza",
            "price": 250,
            "image_url": "pizza.png",
            "is_available": True,
            "is_featured": False,
            "is_vegetarian": True,
            "preparation_time": 20,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Pizza"
    assert data["price"] == "250.00"


async def test_create_menu_item_wrong_owner(client, owner_user, monkeypatch):

    restaurant_id = uuid.uuid4()

    async def mock_get_restaurant(self, restaurant_id):
        return RestaurantResponse(
            id=restaurant_id,
            owner_id="11111111-1111-1111-1111-111111111111",
            status="OPEN",
        )

    monkeypatch.setattr(
        "app.clients.restaurant_client.RestaurantClient.get_restaurant",
        mock_get_restaurant,
    )

    response = await client.post(
        f"/owner/restaurants/{restaurant_id}/menu-items",
        json={
            "name": "Pizza",
            "description": "Cheese Pizza",
            "price": 250,
            "image_url": "pizza.png",
            "is_available": True,
            "is_featured": False,
            "is_vegetarian": True,
            "preparation_time": 20,
        },
    )

    assert response.status_code == 404


async def test_delete_menu_item(client, db, owner_user):
    menu_item = MenuItem(
        restaurant_id=uuid.uuid4(),
        name="Pizza",
        description="Cheese Pizza",
        price=250,
        image_url="pizza.png",
        is_available=True,
        is_featured=False,
        is_vegetarian=True,
        preparation_time=20,
    )

    db.add(menu_item)
    await db.flush()

    item_id = menu_item.id  # capture the ID before the delete invalidates the object

    response = await client.delete(f"/owner/menu-items/{item_id}")
    assert response.status_code == 200

    await db.rollback()  # clear the session's stale state after the app modified it

    result = await db.execute(
        select(MenuItem).where(MenuItem.id == item_id)
    )
    assert result.scalar_one_or_none() is None


async def test_get_available_menu_items(client, db, owner_customer):

    restaurant_id = uuid.uuid4()

    item1 = MenuItem(
        restaurant_id=restaurant_id,
        name="Pizza",
        description="Cheese Pizza",
        price=250,
        image_url="pizza.png",
        is_available=True,
        is_featured=False,
        is_vegetarian=True,
        preparation_time=20,
    )

    item2 = MenuItem(
        restaurant_id=restaurant_id,
        name="Burger",
        description="Chicken Burger",
        price=350,
        image_url="burger.png",
        is_available=False,
        is_featured=False,
        is_vegetarian=False,
        preparation_time=25,
    )

    db.add_all([item1, item2])
    await db.flush()          # ← not commit()

    response = await client.get(f"/restaurants/{restaurant_id}/menu")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Pizza"

    assert len(data) == 1

    assert data[0]["name"] == "Pizza"

    assert data[0]["is_available"] is True