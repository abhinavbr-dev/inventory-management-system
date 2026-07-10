from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class InventoryStrategyBase(ABC):

    @abstractmethod
    def process_sale(
        self,
        db: Session,
        product_id: int,
        quantity: int,
        batch_number: str | None = None
    ):
        pass