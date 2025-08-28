from typing import List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept and store a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection when client disconnects."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific client."""
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        """Send a message to all connected clients."""
        for connection in self.active_connections:
            await connection.send_text(message)
