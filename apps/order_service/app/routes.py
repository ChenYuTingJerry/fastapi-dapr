from fastapi import APIRouter
import httpx

router = APIRouter()

@router.post("/create")
async def create_order():
    # Simulate creating an order
    # Call payment service via Dapr
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:3502/v1.0/invoke/payment-service/method/pay")
    return {"order": "created", "payment_response": response.json()}