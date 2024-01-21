import requests
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/greeting")
async def greeting():
    return {"hello": "world"}


@app.post("/echo")
async def echo(request: Request):
    return await request.json()


@app.post("/hit")
async def hit():
    url = f"http://localhost:3500/v1.0/invoke/pythonapp/method/echo"
    res = requests.post(
        url, json={"koko": "gg"}
    )
    return {"internal": res.text}


if __name__ == "__main__":
    uvicorn.run(app)
