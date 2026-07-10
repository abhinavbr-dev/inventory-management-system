from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.business import Business
from app.models.sale import Sale
from app.models.sale_item import SaleItem

from app.schemas.sale import SaleCreate

from app.strategies.factory import StrategyFactory


class SalesService:

    @staticmethod
    def create_sale(db: Session, sale: SaleCreate):

        try:

            business = db.query(Business).filter(
                Business.id == sale.business_id
            ).first()

            if not business:
                raise HTTPException(
                    status_code=404,
                    detail="Business not found"
                )

            strategy = StrategyFactory.get_strategy(
                business.inventory_strategy
            )

            strategy.process_sale(
                db=db,
                product_id=sale.product_id,
                quantity=sale.quantity,
                batch_number=sale.batch_number
            )

            new_sale = Sale(
                business_id=sale.business_id
            )

            db.add(new_sale)
            db.flush()

            sale_item = SaleItem(
                sale_id=new_sale.id,
                product_id=sale.product_id,
                quantity=sale.quantity
            )

            db.add(sale_item)

            db.commit()
            db.refresh(new_sale)

            return new_sale

        except Exception:
            db.rollback()
            raise