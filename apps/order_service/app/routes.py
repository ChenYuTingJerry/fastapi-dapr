import json
import logging

from dapr.aio.clients import DaprClient
from fastapi import APIRouter
import httpx

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/create")
async def create_order():
    # Simulate creating an order
    # Call payment service via Dapr
    logger.info("️Create oder")
    req_data = {'id': 1, 'message': 'hello world'}
    # async with httpx.AsyncClient() as client:
    #     await client.post(
    #         "http://localhost:3500/v1.0/invoke/payment-service/method/pay",
    #         json=req_data
    #     )
    async with DaprClient() as client:
        resp = await client.invoke_method(
            'payment-service',
            'pay',
            http_verb='POST',
            content_type='application/json',
            data=json.dumps(req_data),
        )
        return {"order": "created", "payment_response": resp.json()}
