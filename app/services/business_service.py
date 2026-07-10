from sqlalchemy.orm import Session

from app.models.business import Business
from app.schemas.business import BusinessCreate


class BusinessService:

    @staticmethod
    def create_business(db: Session, business: BusinessCreate):

        new_business = Business(
            name=business.name,
            inventory_strategy=business.inventory_strategy
        )

        db.add(new_business)
        db.commit()
        db.refresh(new_business)

        return new_business

    @staticmethod
    def get_all_businesses(db: Session):
        return db.query(Business).all()