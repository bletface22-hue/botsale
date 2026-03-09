from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import AutoStockItem


class StockService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upload_lines(self, product_id: int, lines: list[str]) -> int:
        prepared = [line.strip() for line in lines if line.strip()]
        for line in prepared:
            self.session.add(AutoStockItem(product_id=product_id, raw_value=line))
        await self.session.commit()
        return len(prepared)

    async def issue(self, product_id: int, order_id: int, quantity: int) -> list[str]:
        query = (
            select(AutoStockItem)
            .where(AutoStockItem.product_id == product_id, AutoStockItem.is_used.is_(False))
            .limit(quantity)
            .with_for_update(skip_locked=True)
        )
        items = list((await self.session.scalars(query)).all())
        if len(items) < quantity:
            return []
        for item in items:
            item.is_used = True
            item.issued_order_id = order_id
            item.used_at = datetime.utcnow()
        await self.session.commit()
        return [item.raw_value for item in items]
