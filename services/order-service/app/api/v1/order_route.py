from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.core.rate_limiter import rate_limit
from app.dependencies.auth import get_current_user
from app.schemas.order_schema import OrderResponse, OrderDetailResponse, CancelOrderResponse, UpdateOrderStatus
from app.schemas.token_payload import TokenPayload
from app.services.customer_order_service import CustomerOrderService
from app.services.owner_order_service import OwnerOrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

customer_service = CustomerOrderService()
owner_service = OwnerOrderService()


# ----------------------------
# CUSTOMER
# ----------------------------

@router.post("/customer", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    return await customer_service.place_order(db, current_user)


@router.get("/customer", response_model=list[OrderResponse])
async def get_orders(page:int=1, page_size:int=10, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
    return await customer_service.get_orders(page, page_size, db, current_user)


@router.get("/customer/{order_id}", response_model=OrderDetailResponse)
async def get_order(order_id: UUID, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    return await customer_service.get_order(db, order_id, current_user)


@router.put("/customer/{order_id}/cancel", response_model=CancelOrderResponse)
async def cancel_order(order_id: UUID, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    return await customer_service.cancel_order(db, order_id, current_user)


# ----------------------------
# OWNER
# ----------------------------

@router.get("/owner/{restaurant_id}", response_model=list[OrderResponse])
async def get_restaurant_orders(restaurant_id: UUID, page:int=1, page_size:int=10, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user)):
    return await owner_service.get_orders(page, page_size, db, restaurant_id, current_user)


@router.get("/owner/{restaurant_id}/{order_id}", response_model=OrderDetailResponse)
async def get_restaurant_order(restaurant_id: UUID, order_id: UUID, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    return await owner_service.get_order(db, order_id, restaurant_id, current_user)


@router.put("/owner/{restaurant_id}/{order_id}/status", response_model=OrderResponse)
async def update_order_status(restaurant_id: UUID, order_id: UUID, data: UpdateOrderStatus, db: AsyncSession = Depends(get_db), current_user: TokenPayload = Depends(get_current_user), checker:None= Depends(rate_limit(2,60))):
    return await owner_service.update_status(db, order_id, restaurant_id, data, current_user)