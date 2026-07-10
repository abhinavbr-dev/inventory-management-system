from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    inventory_strategy = Column(String(20), default="FIFO")

    products = relationship("Product", back_populates="business")