import requests
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/greeting")
async def greeting():
    return {"msg": "I am checkout!"}


@app.post("/invoke")
async def hit():
    url = f"http://localhost:3500/v1.0/invoke/api-srv/method/echo"
    res = requests.post(url, json={"koko": "gg"})
    return {"internal": res.text}


@app.post("/publish")
async def publish():
    url = f"http://localhost:3500/v1.0/publish/my-pubsub/try"
    res = requests.post(url, json={"message":"Hi I am checkout"})
    return res.status_code, res.text

if __name__ == "__main__":
    uvicorn.run(app)
