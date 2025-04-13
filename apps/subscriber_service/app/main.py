import json

import httpx
from dapr.aio.clients import DaprClient
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, Body
import logging

from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
app = FastAPI()
dapr_app = DaprApp(app)


@dapr_app.subscribe(pubsub="pubsub", topic="payment.success")
async def handle_payment_event(event_data=Body()):
    logger.info("📨 收到 PubSub 訊息：%s", event_data)
    async with DaprClient() as client:
        resp = await client.invoke_method(
            'workflow-service',
            '/workflow/payment-success',
            http_verb='POST',
            content_type='application/json',
            data=json.dumps(event_data),
        )
    # async with httpx.AsyncClient() as client:
    #     await client.post("http://localhos:3502/start-workflow", json=event_data)

