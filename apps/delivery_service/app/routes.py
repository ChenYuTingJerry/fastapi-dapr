from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/deliver")
async def deliver(request: Request):
    data = await request.json()
    print("📦 產品交付中：", data)
    return {"delivery": "done"}
