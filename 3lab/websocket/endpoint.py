from fastapi import APIRouter, WebSocket
from app.websocket.manager import register, unregister

ws_router = APIRouter()

@ws_router.websocket("/{task_id}")
async def ws_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    register(task_id, websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection open
    except:
        unregister(task_id)
