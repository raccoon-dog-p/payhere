from pydantic import BaseModel
from datetime import datetime


class ItemModel(BaseModel):
    category: str | None
    price: int | None
    cost: int | None
    product_name: str | None
    product_detail: str | None
    barcode: int | None
    expiration_date: datetime | None
    size: str | None


class ItemUpdateModel(ItemModel):
    id: int


class ItemDeleteModel(BaseModel):
    id: int


class ItemViewModel(BaseModel):
    id: int


class ItemPagingViewModel(BaseModel):
    page: int


class ItemSearchModel(BaseModel):
    title: str