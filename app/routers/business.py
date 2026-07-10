from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.business import BusinessCreate, BusinessResponse
from app.services.business_service import BusinessService

router = APIRouter(
    prefix="/business",
    tags=["Business"]
)


@router.post("/", response_model=BusinessResponse)
def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    return BusinessService.create_business(db, business)


@router.get("/", response_model=list[BusinessResponse])
def get_businesses(
    db: Session = Depends(get_db)
):
    return BusinessService.get_all_businesses(db)