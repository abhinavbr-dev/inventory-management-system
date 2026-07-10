from pydantic import BaseModel


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int


class SaleItemResponse(BaseModel):
    id: int
    sale_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True