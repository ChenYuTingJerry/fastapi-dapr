from fastapi import FastAPI
from apps.delivery_service.app.routes import router as delivery_router

app = FastAPI()
app.include_router(delivery_router)