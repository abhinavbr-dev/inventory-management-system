from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    business_id = Column(Integer, ForeignKey("businesses.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business")

    sale_items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan"
    )