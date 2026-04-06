from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from schemas import CategoryCreate, CategoryOut, MenuItemCreate, MenuItemOut, OrderCreate, OrderItemCreate, OrderItemOut, OrderItemUpdate, OrderOut
from database import Base, get_db, engine
from models import Category, MenuItem, Order, OrderItem

Base.metadata.create_all(bind=engine)
api_router = APIRouter(prefix='/api/restaurant')

@api_router.post("/categories", response_model=CategoryOut)
def create_category(category_in: CategoryCreate, db = Depends(get_db)):
    category = Category(**category_in.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@api_router.post("/menu_items", response_model=MenuItemOut)
def create_menu(menu_in: MenuItemCreate, db = Depends(get_db)):
    menu = MenuItem(**menu_in.model_dump())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu

@api_router.post("/order_items", response_model=OrderItemOut)
def create_order_item(order_in: OrderItemCreate, db = Depends(get_db)):
    order_item = OrderItem(**order_in.model_dump())
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item

@api_router.post("/orders", response_model=OrderOut)
def create_order(order_in: OrderCreate, db = Depends(get_db)):
    order = Order(**order_in.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@api_router.get("/categories", response_model=list[CategoryOut])
def get_categories(db = Depends(get_db)):
    stmt = select(Category)
    categories = db.scalars(stmt).all()
    return categories

@api_router.get("/menu_items", response_model=list[MenuItemOut])
def get_menu_items(db = Depends(get_db)):
    stmt = select(MenuItem)
    menu_items = db.scalars(stmt).all()
    return menu_items

@api_router.get("/menu_items/{detail}", response_model=list[MenuItemOut])
def get_menu_item(detail: str, db = Depends(get_db)):
    stmt = select(MenuItem).where(MenuItem.name.contains(detail))
    menu_items = db.scalars(stmt).all()
    return menu_items

@api_router.get("/order_items", response_model=list[OrderItemOut])
def get_order_items(db = Depends(get_db)):
    stmt = select(OrderItem)
    order_items = db.scalars(stmt).all()
    return order_items

@api_router.put("/order_items", response_model=OrderItemOut)
def update_order_items(order_in: OrderItemUpdate, db = Depends(get_db)):
    stmt = select(OrderItem)
    order_items = db.scalars(stmt).all()
    return order_items

@api_router.delete("/order_items/{detail}")
def delete_order_items(detail: str, db = Depends(get_db)):
    stmt = select(OrderItem).where(OrderItem.id.contains(detail))
    order_items = db.scalars(stmt).all()
    return order_items

@api_router.get("/orders", response_model=list[OrderOut])
def get_orders(db = Depends(get_db)):
    stmt = select(Order)
    orders = db.scalars(stmt).all()
    return orders

@api_router.get("/orders/{detail}", response_model=list[OrderOut])
def get_order(detail: str, db = Depends(get_db)):
    stmt = select(Order).where(Order.id.contains(detail))
    orders = db.scalars(stmt).all()
    return orders