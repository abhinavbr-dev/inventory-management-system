from datetime import date

from fastapi import HTTPException

from app.models.inventory_batch import InventoryBatch
from app.strategies.base import InventoryStrategyBase


class FEFOStrategy(InventoryStrategyBase):

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
                InventoryBatch.quantity > 0,
                (InventoryBatch.expiry_date == None)
                | (InventoryBatch.expiry_date >= date.today())
            )
            .order_by(InventoryBatch.expiry_date)
            .all()
        )

        if not batches:
            raise HTTPException(
                status_code=404,
                detail="No inventory available"
            )

        remaining = quantity
        deductions = []

        for batch in batches:

            if remaining == 0:
                break

            deduct_qty = min(batch.quantity, remaining)
            batch.quantity -= deduct_qty
            remaining -= deduct_qty

            deductions.append({
                "batch_id": batch.id,
                "batch_number": batch.batch_number,
                "quantity": deduct_qty
            })

        if remaining > 0:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )

        db.flush()

        return deductions