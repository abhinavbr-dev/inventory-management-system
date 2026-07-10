from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class InventoryBatch(Base):
    __tablename__ = "inventory_batches"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"))

    batch_number = Column(String(50), nullable=False)

    quantity = Column(Integer, nullable=False)

    purchase_price = Column(Numeric(10, 2))

    manufacture_date = Column(Date)

    expiry_date = Column(Date)

    product = relationship("Product", back_populates="batches")