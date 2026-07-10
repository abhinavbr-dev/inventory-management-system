from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    name = Column(String(100), nullable=False)
    sku = Column(String(50), unique=True)

    business = relationship("Business", back_populates="products")

    batches = relationship(
    "InventoryBatch",
    back_populates="product",
    cascade="all, delete-orphan"
)