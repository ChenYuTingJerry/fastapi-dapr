from fastapi import FastAPI
from apps.payment_service.app.routes import router as payment_router

app = FastAPI()
app.include_router(payment_router)
