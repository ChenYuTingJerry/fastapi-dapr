import json
import logging

import httpx
from dapr.aio.clients import DaprClient
from fastapi import APIRouter
from starlette.requests import Request

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter()


@router.post("/pay")
async def pay(req: Request):
    body = await req.json()
    logger.info(f"Pay request: body: {body}")
    async with DaprClient() as client:
        order = {"orderId": 12345}
        result = await client.publish_event(
            pubsub_name="pubsub",
            topic_name="payment.success",
            data=json.dumps(order),
            data_content_type="application/json",
        )
        logging.info(f"Published data: {result}")
    # async with httpx.AsyncClient() as client:
    #     await client.post(
    #         "http://localhost:3501/v1.0/publish/pubsub/payment.success",
    #         json={"id": 7, "name": "Bob Jones"}
    #     )
    return {"payment": "success", **body}
