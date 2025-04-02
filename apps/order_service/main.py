from fastapi import FastAPI
from pydantic import BaseModel
from dapr.clients import DaprClient
import requests

app = FastAPI()
client = DaprClient()

class OrderRequest(BaseModel):
    order_id: str
    amount: float

@app.post("/orders")
def create_order(order: OrderRequest):
    # Publish event
    client.publish_event(
        pubsub_name="pubsub",
        topic_name="order-created",
        data=order.model_dump(),
    )

    # Service Invocation to payment service via Dapr gRPC
    response = requests.post(
        url="http://localhost:3500/v1.0/invoke/payment/method/ProcessPayment",
        json=order.model_dump(),
    )
    return {"status": "order sent", "payment_response": response.json()}