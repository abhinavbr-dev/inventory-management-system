from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.inventory_batch import (
    InventoryBatchCreate,
    InventoryBatchResponse
)
from app.services.inventory_service import InventoryService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.post("/", response_model=InventoryBatchResponse)
def create_inventory(
    inventory: InventoryBatchCreate,
    db: Session = Depends(get_db)
):
    return InventoryService.create_inventory(db, inventory)


@router.get("/", response_model=list[InventoryBatchResponse])
def get_inventory(
    db: Session = Depends(get_db)
):
    return InventoryService.get_inventory(db)