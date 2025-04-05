from fastapi import FastAPI
from apps.order_service.app.routes import router as order_router

app = FastAPI()
app.include_router(order_router)