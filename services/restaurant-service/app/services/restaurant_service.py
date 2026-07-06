from uuid import UUID
import json
from app.core.logger import logger
from app.core.redis_component import redis_client
from app.exceptions.all_exceptions import RestaurantNotFound, InvalidRestaurant, NonRestaurantOwner
from sqlalchemy.orm import Session
from app.schemas.token_payload import TokenPayload
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant_schema import RestaurantCreate, RestaurantUpdate, RestaurantStatusUpdate, RestaurantResponse


class RestaurantService:

    @staticmethod
    def create_restaurant(db:Session, current_user: TokenPayload, data: RestaurantCreate):
        if current_user.role != "RESTAURANT_OWNER":
            raise NonRestaurantOwner()
        return RestaurantRepository.create(db=db,owner_id=current_user.sub,data=data)

    @staticmethod
    def get_restaurants_by_owner(db:Session, owen_id:UUID):
        cache_key = f"restaurant:{owen_id}"
        cache_data = redis_client.get(cache_key)
        if cache_data:
            return [RestaurantResponse.model_validate(r) for r in json.loads(cache_data)]
        all = RestaurantRepository.get_by_owner(db=db,owner_id=owen_id)
        if all is None:
            raise RestaurantNotFound()
        response = [RestaurantResponse.model_validate(r) for r in all]
        cache_value = json.dumps([json.loads(r.model_dump_json()) for r in response])
        redis_client.setex(cache_key, 60, cache_value)
        return all


    @staticmethod
    def get_restaurant_by_id(db:Session, restaurant_id: UUID):
        cache_key = f"restaurant:{restaurant_id}"
        cache_data = redis_client.get(cache_key)
        if cache_data:
            return RestaurantResponse.model_validate_json(cache_data)
        restaurant = RestaurantRepository.get_by_id(db, restaurant_id)
        if restaurant is None:
            raise RestaurantNotFound()
        response = RestaurantResponse.model_validate(restaurant)
        redis_client.setex(cache_key, 60, response.model_dump_json())
        return restaurant


    @staticmethod
    def delete_restaurant(db: Session, current_user: TokenPayload, restaurant_id: UUID):
        restaurant = RestaurantRepository.get_by_id(db, restaurant_id)
        if restaurant is None:
            raise RestaurantNotFound()
        if restaurant.owner_id != current_user.sub:
            raise InvalidRestaurant()
        RestaurantRepository.delete_restaurant_by_id(db, restaurant_id)

        return { "message": "Restaurant deleted successfully" }


    @staticmethod
    def update_restaurant(db:Session, current_user: TokenPayload, restaurant_id: UUID, data: RestaurantUpdate):
        restaurant = RestaurantRepository.get_by_id(db, restaurant_id)
        if restaurant is None:
            raise RestaurantNotFound()
        if restaurant.owner_id != current_user.sub:
            raise InvalidRestaurant()

        return RestaurantRepository.update_restaurant_by_data(db, restaurant, data)


    @staticmethod
    def update_status(db:Session, current_user: TokenPayload, restaurant_id: UUID, data: RestaurantStatusUpdate):
        restaurant = RestaurantRepository.get_by_id(db, restaurant_id)
        if restaurant is None:
            raise RestaurantNotFound()
        if restaurant.owner_id != current_user.sub:
            raise InvalidRestaurant()
        return RestaurantRepository.update_restaurant_status(db, restaurant, data.status)
