from pydantic import BaseModel, Field
from app.enums import InventoryStrategy


class BusinessCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    inventory_strategy: InventoryStrategy


class BusinessResponse(BaseModel):
    id: int
    name: str
    inventory_strategy: InventoryStrategy

    model_config = {
        "from_attributes": True
    }