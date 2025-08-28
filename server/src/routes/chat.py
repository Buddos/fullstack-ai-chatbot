from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from ..socket.connection import ConnectionManager
from ..socket.utils import get_token   # ✅ import token dependency

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket, 
    token: str = Depends(get_token)    # ✅ FastAPI validates token automatically
):
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            print(f"Received: {data}")

            # Simulate sending back a response
            await manager.send_personal_message(
                "Response: Simulating response from the GPT service",
                websocket
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)

