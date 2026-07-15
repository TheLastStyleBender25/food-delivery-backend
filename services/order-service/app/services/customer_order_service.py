#place_order()
#get_orders()
#get_order()
#cancel_order()
from app.models import Order, OrderItem
from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.schemas.order_schema import OrderStatus, OrderResponse, OrderItemResponse, CancelOrderResponse, UpdateOrderStatus, OrderDetailResponse
from app.repositories.order_repository import OrderRepository
from app.repositories.order_Item_repository import OrderItemRepository
from app.schemas.token_payload import TokenPayload
from decimal import Decimal
from uuid import UUID
from app.client.cart_client import CartClient
from app.client.menu_client import MenuClient
from pydantic import TypeAdapter
from app.core.redis_component import redis_client
from app.exceptions.all_exceptions import ForbiddenException, CartItemNotFoundException, OrderNotFoundException, CannotCancelOrderException, MenuItemNotFoundException


class CustomerOrderService:

    def __init__(self):
        self.order_repo = OrderRepository()
        self.order_item_repo = OrderItemRepository()
        self.cart_client = CartClient()
        self.menu_client = MenuClient()
        self.order_list_adapter = TypeAdapter(list[OrderResponse])



    async def place_order(self, db: AsyncSession, current_user: TokenPayload) -> OrderResponse:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        cart = await self.cart_client.get_cart(current_user.sub)
        if not cart.items:
            raise CartItemNotFoundException()
        order = Order(customer_id=current_user.sub,restaurant_id=cart.items[0].restaurant_id,total_amount=cart.subtotal)
        order = await self.order_repo.create(db, order)
        for item in cart.items:
            menu_item = await self.menu_client.get_menu_item(item.menu_item_id)
            if not menu_item.is_available:
                raise MenuItemNotFoundException()
            order_item = OrderItem(order_id=order.id,menu_item_id=menu_item.id,name=menu_item.name,quantity=item.quantity,price_at_order=item.price_at_addition)

            await self.order_item_repo.create(db, order_item)

        await db.commit()
        await self.cart_client.clear_cart(current_user.sub)
        await db.refresh(order)
        return OrderResponse.model_validate(order)


    async def get_orders(self,page, page_size, db: AsyncSession,current_user: TokenPayload) -> list[OrderResponse]:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        cache_key = f"get_orders:{page}:{page_size}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return self.order_list_adapter.validate_json(cache_data)
        orders = await self.order_repo.get_customer_orders(db=db,customer_id=current_user.sub)

        start = (page - 1) * page_size
        end = start + page_size
        page_orders = orders[start:end]

        result = [OrderResponse.model_validate(order) for order in page_orders]
        await redis_client.setex(cache_key, 300, self.order_list_adapter.dump_json(result))
        return result


    async def get_order(self,db: AsyncSession,order_id: UUID,current_user: TokenPayload) -> OrderDetailResponse:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        cache_key = f"get_order:{order_id}"
        cache_data = await redis_client.get(cache_key)
        if cache_data:
            return OrderDetailResponse.model_validate_json(cache_data)
        order = await self.order_repo.get_customer_order(db=db,order_id=order_id,customer_id=current_user.sub,)
        if not order:
            raise OrderNotFoundException()
        result = OrderDetailResponse.model_validate(order)
        await redis_client.setex(cache_key, 300, result.model_dump_json())
        return result


    async def cancel_order(self,db: AsyncSession,order_id: UUID,current_user: TokenPayload) -> CancelOrderResponse:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        order = await self.order_repo.get_customer_order(db=db,order_id=order_id,customer_id=current_user.sub)
        if not order:
            raise OrderNotFoundException()
        if order.status != OrderStatus.PLACED:
            raise CannotCancelOrderException()

        order.status = OrderStatus.CANCELLED

        await db.commit()
        await db.refresh(order)

        return CancelOrderResponse(message="Order cancelled successfully.")