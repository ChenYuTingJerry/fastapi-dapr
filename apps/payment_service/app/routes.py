from fastapi import APIRouter
import httpx

router = APIRouter()

@router.post("/pay")
async def pay():
    # Simulate payment
    # Publish payment.success event
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:3502/v1.0/publish/pubsub/payment.success",
            json={"status": "success"}
        )
    return {"payment": "success"}