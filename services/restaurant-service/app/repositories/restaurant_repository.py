from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Restaurant
from app.models.restaurant_status import RestaurantStatus
from app.schemas.restaurant_schema import RestaurantCreate, RestaurantUpdate

class RestaurantRepository:

    @staticmethod
    def create(db : Session, owner_id:UUID, data: RestaurantCreate) -> Restaurant:
        restaurant = Restaurant(
            owner_id=owner_id,
            name=data.name,
            description=data.description,
            phone=data.phone,
            address=data.address,
            city=data.city,
            state=data.state,
            latitude=data.latitude,
            longitude=data.longitude,
            delivery_radius_km=data.delivery_radius_km,
            minimum_order_amount=data.minimum_order_amount,
            average_preparation_time_minutes=data.average_preparation_time_minutes,
            opens_at=data.opens_at,
            closes_at=data.closes_at,
        )

        db.add(restaurant)
        db.commit()
        db.refresh(restaurant)

        return restaurant

    @staticmethod
    def get_by_id(db: Session, restaurant_id: UUID) -> Restaurant | None:
        return (db.query(Restaurant).filter(Restaurant.id == restaurant_id).first())


    @staticmethod
    def get_by_owner(db: Session, owner_id: UUID) -> list[Restaurant]:
        return (db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all())

    @staticmethod
    def delete_restaurant_by_id(db: Session, restaurant_id: UUID):
        db.query(Restaurant).filter(Restaurant.id == restaurant_id).delete()
        db.commit()
        return

    @staticmethod
    def update_restaurant_by_data(db:Session, restaurant:Restaurant, data:RestaurantUpdate):
        if data.name is not None:
            restaurant.name = data.name
        if data.description is not None:
            restaurant.description = data.description
        if data.phone is not None:
            restaurant.phone = data.phone
        if data.address is not None:
            restaurant.address = data.address
        if data.city is not None:
            restaurant.city = data.city
        if data.state is not None:
            restaurant.state = data.state
        db.commit()
        db.refresh(restaurant)

        return restaurant

    @staticmethod
    def update_restaurant_status(db:Session, data: Restaurant, status:RestaurantStatus):
        data.status = status
        db.commit()
        db.refresh(data)
        return data
