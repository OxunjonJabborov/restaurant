from sqlalchemy import ForeignKey, String, Integer, DateTime, Float, DECIMAL, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int]  = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50))
    
    menu_items: Mapped[list['MenuItem']] = relationship(back_populates='category')


class MenuItem(Base):
    __tablename__ = 'menu_items'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    description: Mapped[str] = mapped_column(Text())
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
    category: Mapped['Category'] = relationship(back_populates='menu_items')


class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)
    total: Mapped[float] = mapped_column(DECIMAL(10, 2))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey('menu_items.id'))
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete='CASCADE'), unique=True)
    
    order: Mapped['Order'] = relationship(back_populates='order_items')


class Order(Base):
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(length=13))
    status: Mapped[str]  = mapped_column(String(50))
    
    order_items: Mapped['OrderItem'] = relationship(back_populates='order', cascade='all, delete-orphan')