from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db
from app.core.rate_limiter import rate_limit
from app.schemas.token_payload import TokenPayload
from uuid import UUID
from app.services.cart_service import CartService
from app.schemas.cart_schema import CartItemResponse, CartResponse, CartItemCreate, CartItemUpdate
from app.schemas.internal import InternalCartItemResponse, InternalCartResponse


router = APIRouter(prefix="/cart", tags=["Cart Menu"])

service = CartService()

@router.post("/add", response_model= CartItemResponse)
async def add_item(data: CartItemCreate, db:AsyncSession=Depends(get_db), user: TokenPayload = Depends(get_current_user), checker:None = Depends(rate_limit(20, 60))):
    result = await service.add_item_to_cart(db,data, user)
    return result

@router.get("/get_cart", response_model=CartResponse)
async def get_cart(db:AsyncSession=Depends(get_db), user: TokenPayload = Depends(get_current_user), checker:None = Depends(rate_limit(20, 60))):
    result = await service.get_cart(db,user)
    return result

@router.put("update_cart/{menu_item_id}", response_model=CartItemResponse)
async def update_quantity(menu_item_id: UUID,data: CartItemUpdate,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user),_: None = Depends(rate_limit(20, 60)),):
    return await service.update_quantity(db=db,menu_item_id=menu_item_id,data=data,current_user=current_user)

@router.delete("/items/{menu_item_id}")
async def remove_item(menu_item_id: UUID,db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user),_: None = Depends(rate_limit(20, 60)),):
    await service.remove_item(db, menu_item_id,current_user)


@router.delete("/delete")
async def clear_cart(db: AsyncSession = Depends(get_db),current_user: TokenPayload = Depends(get_current_user), _: None = Depends(rate_limit(10, 60))):
    await service.clear_cart(db=db,current_user=current_user)



@router.get("/internal/cart/{customer_id}",response_model=InternalCartResponse)
async def get_internal_cart(customer_id: UUID,db: AsyncSession = Depends(get_db)):
    return await service.get_internal_cart(db, customer_id)

@router.delete("/internal/cart/{customer_id}")
async def clear_internal_cart(customer_id: UUID,db: AsyncSession = Depends(get_db)):
    return await service.clear_internal_cart(db, customer_id)


