from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.inventory_batch import InventoryBatch
from app.models.product import Product
from app.schemas.inventory_batch import InventoryBatchCreate


class InventoryService:

    @staticmethod
    def create_inventory(db: Session, inventory: InventoryBatchCreate):

        # Check if product exists
        product = db.query(Product).filter(
            Product.id == inventory.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        # Check expiry date
        if inventory.expiry_date <= inventory.manufacture_date:
            raise HTTPException(
                status_code=400,
                detail="Expiry date must be after manufacture date"
            )

        # Check duplicate batch number for the same product
        existing_batch = (
            db.query(InventoryBatch)
            .filter(
                InventoryBatch.product_id == inventory.product_id,
                InventoryBatch.batch_number == inventory.batch_number
            )
            .first()
        )

        if existing_batch:
            raise HTTPException(
                status_code=400,
                detail="Batch number already exists for this product"
            )

        new_batch = InventoryBatch(
            product_id=inventory.product_id,
            batch_number=inventory.batch_number,
            quantity=inventory.quantity,
            purchase_price=inventory.purchase_price,
            manufacture_date=inventory.manufacture_date,
            expiry_date=inventory.expiry_date
        )

        db.add(new_batch)
        db.commit()
        db.refresh(new_batch)

        return new_batch

    @staticmethod
    def get_inventory(db: Session):
        return db.query(InventoryBatch).all()