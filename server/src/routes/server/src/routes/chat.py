from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from socket.connection import ConnectionManager  # import your manager

router = APIRouter()
manager = ConnectionManager()  # initialize

@router.websocket("/chat")
async def chat_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client disconnected")
