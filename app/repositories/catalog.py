from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import CatalogCategory, Product


class CatalogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_visible_categories(self) -> list[CatalogCategory]:
        query = (
            select(CatalogCategory)
            .where(CatalogCategory.is_active.is_(True), CatalogCategory.is_visible.is_(True))
            .order_by(CatalogCategory.sort_order.asc())
        )
        rows = await self.session.scalars(query)
        return list(rows)

    async def list_visible_products_by_category(self, category_id: int) -> list[Product]:
        query = (
            select(Product)
            .where(
                Product.category_id == category_id,
                Product.is_active.is_(True),
                Product.is_visible_in_catalog.is_(True),
            )
            .order_by(Product.sort_order.asc())
        )
        rows = await self.session.scalars(query)
        return list(rows)

    async def get_product(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)
