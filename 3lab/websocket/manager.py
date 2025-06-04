from fastapi.websockets import WebSocket
from typing import Dict, List

connections = {}

def register(task_id: str, ws: WebSocket):
    connections[task_id] = ws

def unregister(task_id: str):
    connections.pop(task_id, None)

def notify_client(task_id: str, message: dict):
    ws = connections.get(task_id)
    if ws:
        import asyncio
        asyncio.run(ws.send_json(message))

async def notify(task_id: str, message: str):
    if task_id in connections:
        for ws in connections[task_id]:
            await ws.send_text(message)