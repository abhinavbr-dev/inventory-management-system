from fastapi import HTTPException

from app.models.inventory_batch import InventoryBatch
from app.strategies.base import InventoryStrategyBase


class FIFOStrategy(InventoryStrategyBase):

    def process_sale(
        self,
        db,
        product_id,
        quantity,
        batch_number=None
    ):

        batches = (
            db.query(InventoryBatch)
            .filter(
                InventoryBatch.product_id == product_id,
                InventoryBatch.quantity > 0
            )
            .order_by(InventoryBatch.manufacture_date)
            .all()
        )

        if not batches:
            raise HTTPException(
                status_code=404,
                detail="No inventory available"
            )

        remaining = quantity

        for batch in batches:

            if remaining == 0:
                break

            if batch.quantity >= remaining:

                batch.quantity -= remaining

                remaining = 0

            else:

                remaining -= batch.quantity

                batch.quantity = 0

        if remaining > 0:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        db.flush()