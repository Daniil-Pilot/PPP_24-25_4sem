from fastapi import FastAPI, Request, HTTPException
from app.api.router import api_router
from app.websocket.endpoint import ws_router
from app.websocket.manager import notify

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")

@app.post("/notify/{task_id}")
async def send_notification(task_id: str, request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    if not data:
        raise HTTPException(status_code=400, detail="Empty JSON body")


    await notify(task_id, data)

    return {"status": "ok"}
