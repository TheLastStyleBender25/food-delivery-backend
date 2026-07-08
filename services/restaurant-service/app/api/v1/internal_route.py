from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.internal import InternalRestaurantResponse
from app.services.restaurant_service import RestaurantService

router = APIRouter(prefix="/internal", tags=["Internal"])

@router.get("/restaurants/{restaurant_id}",response_model=InternalRestaurantResponse)
def get_restaurant(restaurant_id: UUID,db: Session = Depends(get_db),):
    return RestaurantService.get_restaurant_internal(db,restaurant_id,)