from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    product_id: int
    product_name: Optional[str] = None
    price: Optional[str] = None
    benefits: Optional[str] = None
    available: Optional[bool] = None
    instructions: Optional[str] = None
    skin_type: Optional[str] = None
    ingredients: Optional[list] = None
    image: Optional[str] = None
    checkout_url: Optional[str] = None
