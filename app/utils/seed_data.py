from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import CatalogCategory, DeliveryMode, Product


async def seed_start_catalog(session: AsyncSession) -> None:
    await session.execute(delete(Product))
    await session.execute(delete(CatalogCategory))

    categories = [
        CatalogCategory(name="SIM", code="sim", sort_order=10),
        CatalogCategory(name="ESIM / Готовый QR-код", code="esim", sort_order=20),
        CatalogCategory(name="ГОСУСЛУГИ", code="gos", sort_order=30),
        CatalogCategory(name="ВЕРИФЫ", code="verif", sort_order=40),
        CatalogCategory(name="SECONDARY_GU", code="secondary_gu", is_visible=False, sort_order=100),
    ]
    session.add_all(categories)
    await session.flush()

    by_code = {c.code: c.id for c in categories}
    products = [
        Product(category_id=by_code["sim"], name="МТС", price=13, delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["sim"], name="Билайн 1к1", price=15, delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["sim"], name="Билайн 2к1", price=17, delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["sim"], name="Билайн 3к1", price=19, delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["sim"], name="Т2 1к1", price=11, delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["sim"], name="Мегафон/Йота", price=8, short_description="Лимит на ГУ 2 SIM", delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["esim"], name="Любой оператор", price=26, delivery_mode=DeliveryMode.icc_id_chat),
        Product(category_id=by_code["gos"], name="ЧИСТ. ГУ БЕЗ OZON", price=42, delivery_mode=DeliveryMode.bot_chat),
        Product(category_id=by_code["gos"], name="ЧИСТ. ГУ + ЧИСТ OZON", price=75, delivery_mode=DeliveryMode.bot_chat),
        Product(category_id=by_code["verif"], name="ВЕРИФИКАЦИЯ ПО ГУ", price=16, short_description="ЯПЭЙ/WB/ЦУПИС/ЮМАНИ", delivery_mode=DeliveryMode.bot_chat),
    ]
    session.add_all(products)
    await session.commit()
