from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CategoryBase(SchemaBase):
    name: str = Field(max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int = Field(ge=1)


class MenuItemBase(SchemaBase):
    name: str = Field(max_length=50)
    price: float = Field(ge=0)
    description: str
    category_id: int = Field(ge=1)


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemOut(MenuItemBase):
    id: int = Field(ge=1)


class OrderItemBase(SchemaBase):
    quantity: int = Field(ge=1)
    total: float = Field(ge=0)


class OrderItemCreate(OrderItemBase):
    menu_item_id: int = Field(ge=1)
    order_id: int = Field(ge=1)


class OrderItemOut(OrderItemBase):
    id: int = Field(ge=1)
    menu_item_id: int = Field(ge=1)
    order_id: int = Field(ge=1)


class OrderItemUpdate(OrderItemBase):
    quantity: int = Field(ge=1)
    total: float = Field(ge=0)


class OrderBase(SchemaBase):
    address: str = Field(max_length=100)
    phone_number: str = Field(max_length=13)
    status: str = Field(max_length=50)


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int = Field(ge=1)
