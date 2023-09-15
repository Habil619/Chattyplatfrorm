from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

active_connections: List[WebSocket] = []

@app.websocket("/ws/{user_id}")
async def connect_websocket(websocket: WebSocket, user_id: int):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(f"User {user_id}: {message}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
