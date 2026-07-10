from fastapi import HTTPException

from app.models.inventory_batch import InventoryBatch
from app.strategies.base import InventoryStrategyBase


class BatchStrategy(InventoryStrategyBase):

    def process_sale(
        self,
        db,
        product_id,
        quantity,
        batch_number=None
    ):

        if not batch_number:
            raise HTTPException(
                status_code=400,
                detail="Batch number is required"
            )

        batch = (
            db.query(InventoryBatch)
            .filter(
                InventoryBatch.product_id == product_id,
                InventoryBatch.batch_number == batch_number
            )
            .first()
        )

        if not batch:
            raise HTTPException(
                status_code=404,
                detail="Batch not found"
            )

        if batch.quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock in selected batch"
            )

        batch.quantity -= quantity

        db.flush()