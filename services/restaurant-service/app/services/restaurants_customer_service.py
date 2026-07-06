from uuid import UUID
from sqlalchemy.orm import Session
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.token_payload import TokenPayload
from app.schemas.restaurant_customer_schema import NearByRestaurantResponse, GetCustomerLocationRequest, CustomerRestaurantDetailResponse
from app.exceptions.all_exceptions import NonCustomerException, RestaurantNotFound, RestaurantNotOpenException
from app.core.distance_calculator import calculate_distance_in_kn
from app.repositories.retsaurant_customer_repository import RestaurantCustomerRepository
from app.core.redis_component import redis_client
import json


class RestaurantCustomerService:

    @staticmethod
    def get_all_restaurants_in_range(db:Session, data:GetCustomerLocationRequest, current_user:TokenPayload, page, size,  max_preparation_time: int | None = None, max_minimum_order_amount:float |None = None):
        if current_user.role != "CUSTOMER":
            raise NonCustomerException()
        cache_key = (f"nearby:"f"{round(data.latitude, 4)}:"f"{round(data.longitude, 4)}:"f"{page}:"f"{size}:"f"{max_preparation_time}:"f"{max_minimum_order_amount}")
        cache_data = redis_client.get(cache_key)
        if cache_data:
            cached_restaurants = json.loads(cache_data)
            return [NearByRestaurantResponse.model_validate(r) for r in cached_restaurants]
        restaurants  = RestaurantCustomerRepository.get_all_open_restaurants(db=db)

        if not restaurants:
            redis_client.setex(cache_key, 60, "[]")
            return []

        near_by = []
        start = (page - 1) * size
        end = start + size
        for restaurant in restaurants:
            distance = calculate_distance_in_kn(data.latitude, data.longitude, restaurant.latitude, restaurant.longitude)
            if distance > restaurant.delivery_radius_km:
                continue
            # Preparation time filter
            if (max_preparation_time is not None and restaurant.average_preparation_time_minutes > max_preparation_time):
                continue
            # Minimum order filter
            if (max_minimum_order_amount is not None and restaurant.minimum_order_amount > max_minimum_order_amount):
                continue

            near = NearByRestaurantResponse(id=restaurant.id, name=restaurant.name, description=restaurant.description,
                                            minimum_order_amount=restaurant.minimum_order_amount,
                                            average_preparation_time_minutes=restaurant.average_preparation_time_minutes)
            near_by.append(near)

        paginated_result = near_by[start:end]

        serialized_data = [restaurant.model_dump(mode="json") for restaurant in paginated_result]

        redis_client.setex(cache_key,60,json.dumps(serialized_data))

        return paginated_result



    @staticmethod
    def get_restaurant_by_id(current_user:TokenPayload, db:Session, restaurant_id:UUID):
        cache_key = f"restaurants:{restaurant_id}"
        cache_data = redis_client.get(cache_key)
        if cache_data:
            return CustomerRestaurantDetailResponse.model_validate_json(cache_data)

        if current_user.role != "CUSTOMER":
            raise NonCustomerException()
        restaurant = RestaurantRepository.get_by_id(db, restaurant_id)
        if restaurant is None:
            raise RestaurantNotFound()
        if restaurant.status != "OPEN":
            raise RestaurantNotOpenException()

        response = CustomerRestaurantDetailResponse.model_validate(restaurant)
        redis_client.setex(cache_key, 60, response.model_dump_json())

        return restaurant






