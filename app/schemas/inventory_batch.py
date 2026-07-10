from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class InventoryBatchCreate(BaseModel):
    product_id: int

    batch_number: str = Field(..., min_length=1, max_length=50)

    quantity: int = Field(..., gt=0)

    purchase_price: Decimal = Field(..., gt=0)

    manufacture_date: date
    expiry_date: date


class InventoryBatchResponse(BaseModel):
    id: int
    product_id: int
    batch_number: str
    quantity: int
    purchase_price: Decimal
    manufacture_date: date
    expiry_date: date

    model_config = {
        "from_attributes": True
    }