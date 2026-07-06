from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.logger import logger
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.repositories.restaurant_repository import RestaurantRepository
from app.schemas.restaurant_schema import RestaurantCreate, RestaurantResponse, RestaurantUpdate, RestaurantStatusUpdate
from app.schemas.restaurant_customer_schema import NearByRestaurantResponse, GetCustomerLocationRequest, CustomerRestaurantDetailResponse
from app.schemas.token_payload import TokenPayload
from app.services.restaurant_service import RestaurantService
from app.services.restaurants_customer_service import RestaurantCustomerService
from app.core.rate_limiter import rate_limit

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.post("/create", response_model=RestaurantResponse)
def create_restaurant(data: RestaurantCreate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None=Depends(rate_limit(2,60))):
    return RestaurantService.create_restaurant(db, current_user, data)


@router.get("/", response_model=list[RestaurantResponse])
def get_my_restaurants(db : Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None=Depends(rate_limit(2,60))):
    return RestaurantService.get_restaurants_by_owner(db, current_user.sub)

@router.get("/{restaurant_id}/all", response_model=RestaurantResponse)
def get_restaurant_from_id(restaurant_id:UUID, db:Session=Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None=Depends(rate_limit(2,60))):
    return RestaurantService.get_restaurant_by_id(db, restaurant_id)

@router.delete("/{restaurant_id}/id")
def delete_restaurant_from_id(restaurant_id:UUID ,db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None=Depends(rate_limit(2,60))):
    return RestaurantService.delete_restaurant(db, current_user, id)

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant_data(restaurant_id:UUID, data: RestaurantUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None=Depends(rate_limit(2,60))):
    return RestaurantService.update_restaurant(db, current_user, restaurant_id, data)

@router.patch("/{restaurant_id}/status", response_model=RestaurantResponse)
def update_status_restaurant(restaurant_id:UUID, data:RestaurantStatusUpdate, db: Session = Depends(get_db), current_user: TokenPayload = Depends(get_current_user),checker:None=Depends(rate_limit(2,60))):
    return RestaurantService.update_status(db, current_user, restaurant_id, data)

@router.get("/get_nearby_restaurants", response_model=list[NearByRestaurantResponse])
def get_nearby_restaurants(latitude: float, longitude: float, page:int = 1, page_size:int = 10, db:Session=Depends(get_db), current_user: TokenPayload = Depends(get_current_user), max_preparation_time: int | None = None, max_minimum_order_amount:float |None = None):
    location = GetCustomerLocationRequest(latitude=latitude, longitude=longitude)
    return RestaurantCustomerService.get_all_restaurants_in_range(db, location, current_user, page, page_size, max_preparation_time, max_minimum_order_amount)

@router.get("/search_restaurant", response_model=CustomerRestaurantDetailResponse)
def search_restaurant(id:UUID, db:Session=Depends(get_db), current_user:TokenPayload = Depends(get_current_user), checker:None=Depends(rate_limit(2,60))):
    return RestaurantCustomerService.get_restaurant_by_id(current_user, db, id)

@router.get("/checker")
def test_rate_limiter(checker:None=Depends(rate_limit(2,60))):
    return {"message":"Rate Limit Exceeded!"}