from uuid import UUID
from sqlalchemy.orm import Session
from app.models import Restaurant
from app.models.restaurant_status import RestaurantStatus

class RestaurantCustomerRepository:

    @staticmethod
    def get_all_open_restaurants(db:Session) -> list[Restaurant]:
        return (db.query(Restaurant).filter(Restaurant.status == RestaurantStatus.OPEN).all())


    @staticmethod
    def _get_by_id(db:Session, id:UUID) -> Restaurant:
        return (db.query(Restaurant).filter(Restaurant.id == id).first())
