from fastapi import FastAPI
from app.database import Base, engine
import app.models
from app.routers.business import router as business_router
from app.routers.product import router as product_router
from app.routers.inventory import router as inventory_router
from app.routers.sales import router as sales_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Management API")

app.include_router(business_router)

app.include_router(product_router)

app.include_router(inventory_router)

app.include_router(sales_router)

@app.get("/")
def root():
    return {"message": "Inventory Management API is running"}