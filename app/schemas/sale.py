from pydantic import BaseModel


class SaleCreate(BaseModel):
    business_id: int
    product_id: int
    quantity: int
    batch_number: str | None = None


class SaleResponse(BaseModel):
    id: int
    business_id: int

    class Config:
        from_attributes = True