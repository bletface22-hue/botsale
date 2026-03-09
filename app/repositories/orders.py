from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import DeliveryMode, Order, OrderStatus


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_order(self, user_id: int, product_id: int, amount: float, delivery_mode: DeliveryMode) -> Order:
        count_query = select(func.count(Order.id))
        count = (await self.session.execute(count_query)).scalar_one()
        order = Order(
            order_number=f"ORD-{count + 1:06d}",
            user_id=user_id,
            product_id=product_id,
            amount=amount,
            delivery_mode=delivery_mode,
            status=OrderStatus.waiting_payment,
        )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def mark_paid(self, order: Order) -> Order:
        order.status = OrderStatus.paid
        order.paid_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def save_iccid(self, order: Order, iccid_text: str) -> Order:
        order.iccid_text = iccid_text
        order.status = OrderStatus.iccid_received
        await self.session.commit()
        await self.session.refresh(order)
        return order
