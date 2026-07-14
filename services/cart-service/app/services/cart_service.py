from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.schemas.cart_schema import CartItemCreate, CartResponse, CartItemResponse, CartItemUpdate
from app.repositories.cart_repository import CartRepository
from app.schemas.token_payload import TokenPayload
from app.clients.menu_client import MenuClient
from app.models.cart_item import CartItem
from decimal import Decimal
from uuid import UUID
from app.exceptions.all_exceptions import ForbiddenException, MenuItemNotFoundException, DifferentRestaurantException, CartItemNotFoundException


class CartService:

    def __init__(self):
        self.repo = CartRepository()
        self.menu_client = MenuClient()


    async def add_item_to_cart(self, db: AsyncSession, data: CartItemCreate, current_user: TokenPayload) -> CartItemResponse:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        menu_item = await self.menu_client.get_menu_item(data.menu_item_id)
        if not menu_item.is_available:
            raise MenuItemNotFoundException()

        existing = await self.repo.get_cart_item(db, current_user.sub, data.menu_item_id)
        if existing:
            existing.quantity += data.quantity
            await db.commit()
            await db.refresh(existing)
            return existing

        customer_cart = await self.repo.get_customer_cart(db,current_user.sub)

        if customer_cart:
            if customer_cart[0].restaurant_id != menu_item.restaurant_id:
                raise DifferentRestaurantException()

        cart_item = CartItem(customer_id=current_user.sub,restaurant_id=menu_item.restaurant_id, menu_item_id=data.menu_item_id, quantity=data.quantity, price_at_addition=menu_item.price)
        cart_item = await self.repo.create(db, cart_item)

        await db.commit()

        return CartItemResponse.model_validate(cart_item)

    async def get_cart(self,db: AsyncSession,current_user: TokenPayload,) -> CartItemResponse:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        items = await self.repo.get_customer_cart(db,current_user.sub)
        subtotal = Decimal("0")
        responses:list[CartItemResponse] = []
        for item in items:
            subtotal += item.price_at_addition * item.quantity
            responses.append(CartItemResponse.model_validate(item))

        return CartResponse(items=responses,subtotal=subtotal)


    async def remove_item(self, db: AsyncSession, menu_item_id: UUID, current_user: TokenPayload,) -> None:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        cart_item = await self.repo.get_cart_item(db=db,customer_id=current_user.sub, menu_item_id=menu_item_id)
        if cart_item is None:
            raise CartItemNotFoundException()

        await self.repo.delete(db, cart_item)
        await db.commit()


    async def clear_cart(self, db: AsyncSession, current_user: TokenPayload) -> None:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        await self.repo.clear_cart(db=db,customer_id=current_user.sub)

        await db.commit()

    async def update_quantity(self,db: AsyncSession,menu_item_id: UUID,data: CartItemUpdate,current_user: TokenPayload) -> CartItemResponse:
        if current_user.role != "CUSTOMER":
            raise ForbiddenException()
        cart_item = await self.repo.get_cart_item( db=db, customer_id=current_user.sub, menu_item_id=menu_item_id,)
        if cart_item is None:
            raise CartItemNotFoundException()
        cart_item.quantity = data.quantity

        await db.commit()
        await db.refresh(cart_item)

        return CartItemResponse.model_validate(cart_item)

    async def get_internal_cart(self, db: AsyncSession,customer_id: UUID):
        cart_items = await self.repo.get_customer_cart(db,customer_id)

        subtotal = Decimal("0.00")
        items = []
        for item in cart_items:
            subtotal += item.price_at_addition * item.quantity

            items.append(
                InternalCartItemResponse(
                    restaurant_id=item.restaurant_id,
                    menu_item_id=item.menu_item_id,
                    quantity=item.quantity,
                    price_at_addition=item.price_at_addition,
                )
            )

            return InternalCartResponse(items=items,subtotal=subtotal)

    async def clear_internal_cart(self,db: AsyncSession,customer_id: UUID):
        await self.repo.clear_cart(db,customer_id)
        await db.commit()

        return {"Cart cleared successfully"}








