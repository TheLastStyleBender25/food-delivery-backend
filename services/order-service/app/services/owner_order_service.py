from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions.all_exceptions import (
    ForbiddenException,
    OrderNotFoundException,
)
from app.models.order_status import OrderStatus
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import (
    OrderResponse,
    OrderDetailResponse,
    UpdateOrderStatus,
)
from app.schemas.token_payload import TokenPayload
from app.core.redis_component import redis_client
from pydantic import TypeAdapter




class OwnerOrderService:

    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_list_adapter = TypeAdapter(list[OrderResponse])


    async def get_orders(self, page:int, page_size:int, db: AsyncSession,restaurant_id: UUID,current_user: TokenPayload) -> list[OrderResponse]:
        if current_user.role != "RESTAURANT_OWNER":
            raise ForbiddenException()
        cache_key = f"get_orders:{page}:{page_size}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return self.order_list_adapter.validate_json(cache_data)
        orders = await self.order_repo.get_restaurant_orders(db=db,restaurant_id=restaurant_id)

        start = (page - 1) * page_size
        end = start + page_size
        page_orders = orders[start:end]

        result = [OrderResponse.model_validate(order) for order in page_orders]
        await redis_client.setex(cache_key, 300, self.order_list_adapter.dump_json(result))
        return result


    async def get_order(self,db: AsyncSession,order_id: UUID,restaurant_id: UUID,current_user: TokenPayload) -> OrderDetailResponse:
        if current_user.role != "RESTAURANT_OWNER":
            raise ForbiddenException()

        cache_key = f"get_order:{order_id}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return OrderDetailResponse.model_validate_json(cache_data)
        order = await self.order_repo.get_restaurant_order(db=db,order_id=order_id,restaurant_id=restaurant_id)

        if not order:
            raise OrderNotFoundException()

        response =  OrderDetailResponse.model_validate(order)
        await redis_client.setex(cache_key, 300, response.model_dump_json())
        return response


    async def update_status(self,db: AsyncSession,order_id: UUID,restaurant_id: UUID,data: UpdateOrderStatus,current_user: TokenPayload) -> OrderResponse:
        if current_user.role != "RESTAURANT_OWNER":
            raise ForbiddenException()

        order = await self.order_repo.get_restaurant_order(db=db,order_id=order_id,restaurant_id=restaurant_id)

        if not order:
            raise OrderNotFoundException()

        order.status = data.status

        await db.commit()
        await db.refresh(order)

        return OrderResponse.model_validate(order)