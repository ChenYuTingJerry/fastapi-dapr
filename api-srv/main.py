import uvicorn
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()
dapr_app = DaprApp(app)


class CloudEvent(BaseModel):
    datacontenttype: str
    source: str
    topic: str
    pubsubname: str
    data: dict
    id: str
    specversion: str
    tracestate: str
    type: str
    traceid: str


@app.get("/greeting")
async def greeting():
    return {"msg": "I am api!"}


@app.post("/echo")
async def echo(request: Request):
    return await request.json()


# Dapr subscription routes orders topic to this route
@dapr_app.subscribe(pubsub="my-pubsub", topic="try")
def try_subscriber(event: CloudEvent):
    print("Subscriber received : %s" % event.model_dump_json(), flush=True)
    return {"success": True}


if __name__ == "__main__":
    uvicorn.run(app)
