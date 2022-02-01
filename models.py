from typing import List
from pydantic import BaseModel, Field


class Request(BaseModel):
    base64: str

class SimpleMenu(BaseModel):
    name: str = Field(..., title="name", description="Dish name")
    price: str = Field(..., title="price", description="Price of the dish")


class DescriptionMenu(BaseModel):
    name: str = Field(..., title="name", description="Dish name")
    price: str = Field(..., title="price", description="Price of the dish")
    description: str = Field(..., title="description", description="Description of the dish")


class SimpleMenuResponseModel(BaseModel):
    menus: List[SimpleMenu]


class DescriptionMenuResponseModel(BaseModel):
    menus: List[DescriptionMenu]
