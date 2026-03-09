from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Role(str, Enum):
    buyer = "buyer"
    worker = "worker"
    admin = "admin"


class DeliveryMode(str, Enum):
    icc_id_chat = "icc_id_chat"
    bot_chat = "bot_chat"
    auto_delivery = "auto_delivery"


class OrderStatus(str, Enum):
    new = "new"
    waiting_payment = "waiting_payment"
    paid = "paid"
    waiting_iccid = "waiting_iccid"
    iccid_received = "iccid_received"
    assigned = "assigned"
    in_work = "in_work"
    in_dialogue = "in_dialogue"
    waiting_documents = "waiting_documents"
    completed = "completed"
    canceled = "canceled"
    overdue = "overdue"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    rating_avg: Mapped[float] = mapped_column(Numeric(3, 2), default=0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    orders_count: Mapped[int] = mapped_column(Integer, default=0)
    completed_orders_count: Mapped[int] = mapped_column(Integer, default=0)
    replacements_count: Mapped[int] = mapped_column(Integer, default=0)
    topups_count: Mapped[int] = mapped_column(Integer, default=0)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role_name: Mapped[Role] = mapped_column(SQLEnum(Role), default=Role.buyer)


class CatalogCategory(Base):
    __tablename__ = "catalog_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(64), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=100)


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("catalog_categories.id"))
    name: Mapped[str] = mapped_column(String(255))
    short_description: Mapped[str | None] = mapped_column(String(400), nullable=True)
    full_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    photo_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2))
    fixed_amounts_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    delivery_mode: Mapped[DeliveryMode] = mapped_column(SQLEnum(DeliveryMode), index=True)
    is_visible_in_catalog: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=100)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    selected_options_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.new)
    assigned_worker_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    delivery_mode: Mapped[DeliveryMode] = mapped_column(SQLEnum(DeliveryMode))
    iccid_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deadline_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AutoStockItem(Base):
    __tablename__ = "auto_stock_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    raw_value: Mapped[str] = mapped_column(Text)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    used_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    issued_order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id"), nullable=True)


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class UIText(Base):
    __tablename__ = "ui_texts"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_key: Mapped[str] = mapped_column(String(128), unique=True)
    text_value: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)


class UIButton(Base):
    __tablename__ = "ui_buttons"

    id: Mapped[int] = mapped_column(primary_key=True)
    system_key: Mapped[str] = mapped_column(String(128), unique=True)
    label: Mapped[str] = mapped_column(String(128))
    parent_section: Mapped[str] = mapped_column(String(64), index=True)
    action_type: Mapped[str] = mapped_column(String(64))
    role_scope: Mapped[str] = mapped_column(String(64), default="buyer")
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=100)
