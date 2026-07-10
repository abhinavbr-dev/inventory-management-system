from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    sku: str = Field(..., min_length=2, max_length=50)


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str

    model_config = {
        "from_attributes": True
    }