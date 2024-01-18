import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/greeting")
async def root():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app)
