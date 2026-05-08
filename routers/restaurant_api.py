from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Category, MenuItem, Order, OrderItem
from schemas import (
    CategoryCreate,
    CategoryOut,
    MenuItemCreate,
    MenuItemOut,
    OrderCreate,
    OrderItemCreate,
    OrderItemOut,
    OrderItemUpdate,
    OrderOut,
)


restaurant_api_router = APIRouter(prefix='/api/restaurant')
DbSession = Annotated[AsyncSession, Depends(get_db)]


@restaurant_api_router.post("/categories", response_model=CategoryOut)
async def create_category(category_in: CategoryCreate, db: DbSession):
    stmt = select(Category).where(Category.name == category_in.name)
    existing_category = await db.scalar(stmt)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu kategoriya allaqachon mavjud.",
        )

    category = Category(**category_in.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


@restaurant_api_router.post("/menu_items", response_model=MenuItemOut)
async def create_menu(menu_in: MenuItemCreate, db: DbSession):
    category = await db.get(Category, menu_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category topilmadi")

    stmt = select(MenuItem).where(MenuItem.name == menu_in.name)
    existing_menu = await db.scalar(stmt)
    if existing_menu:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu menu item allaqachon mavjud.",
        )

    menu = MenuItem(**menu_in.model_dump())
    db.add(menu)
    await db.commit()
    await db.refresh(menu)
    return menu


@restaurant_api_router.post("/order_items", response_model=OrderItemOut)
async def create_order_item(order_in: OrderItemCreate, db: DbSession):
    menu_item = await db.get(MenuItem, order_in.menu_item_id)
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item topilmadi")

    order = await db.get(Order, order_in.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order topilmadi")

    stmt = select(OrderItem).where(
        OrderItem.menu_item_id == order_in.menu_item_id,
        OrderItem.order_id == order_in.order_id,
    )
    existing_order_item = await db.scalar(stmt)
    if existing_order_item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu order item allaqachon mavjud.",
        )

    order_item = OrderItem(**order_in.model_dump())
    db.add(order_item)
    await db.commit()
    await db.refresh(order_item)
    return order_item


@restaurant_api_router.post("/orders", response_model=OrderOut)
async def create_order(order_in: OrderCreate, db: DbSession):
    order = Order(**order_in.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


@restaurant_api_router.get("/categories", response_model=list[CategoryOut])
async def get_categories(db: DbSession):
    stmt = select(Category)
    categories = await db.scalars(stmt)
    return categories.all()


@restaurant_api_router.get("/menu_items", response_model=list[MenuItemOut])
async def get_menu_items(db: DbSession):
    stmt = select(MenuItem)
    menu_items = await db.scalars(stmt)
    return menu_items.all()


@restaurant_api_router.get("/menu_items/{detail}", response_model=list[MenuItemOut])
async def get_menu_item(detail: str, db: DbSession):
    stmt = select(MenuItem).where(MenuItem.name.contains(detail))
    menu_items = await db.scalars(stmt)
    return menu_items.all()


@restaurant_api_router.get("/order_items", response_model=list[OrderItemOut])
async def get_order_items(db: DbSession):
    stmt = select(OrderItem)
    order_items = await db.scalars(stmt)
    return order_items.all()


@restaurant_api_router.get("/orders", response_model=list[OrderOut])
async def get_orders(db: DbSession):
    stmt = select(Order)
    orders = await db.scalars(stmt)
    return orders.all()


@restaurant_api_router.get("/orders/{order_id}", response_model=OrderOut)
async def get_order(order_id: int, db: DbSession):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order topilmadi")
    return order


@restaurant_api_router.put("/order_items/{item_id}", response_model=OrderItemOut)
async def update_order_item(item_id: int, order_in: OrderItemUpdate, db: DbSession):
    item = await db.get(OrderItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order item topilmadi")

    item.quantity = order_in.quantity
    item.total = order_in.total
    await db.commit()
    await db.refresh(item)
    return item


@restaurant_api_router.delete("/categories/{item_id}")
async def delete_category(item_id: int, db: DbSession):
    item = await db.get(Category, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Category topilmadi")

    await db.delete(item)
    await db.commit()
    return {"detail": f"Category {item_id} o'chirildi"}


@restaurant_api_router.delete("/menu_items/{item_id}")
async def delete_menu_item(item_id: int, db: DbSession):
    item = await db.get(MenuItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item topilmadi")

    await db.delete(item)
    await db.commit()
    return {"detail": f"Menu item {item_id} o'chirildi"}


@restaurant_api_router.delete("/order_items/{item_id}")
async def delete_order_item(item_id: int, db: DbSession):
    item = await db.get(OrderItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order item topilmadi")

    await db.delete(item)
    await db.commit()
    return {"detail": f"Order item {item_id} o'chirildi"}


@restaurant_api_router.delete("/orders/{item_id}")
async def delete_order(item_id: int, db: DbSession):
    item = await db.get(Order, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Order topilmadi")

    await db.delete(item)
    await db.commit()
    return {"detail": f"Order {item_id} o'chirildi"}
