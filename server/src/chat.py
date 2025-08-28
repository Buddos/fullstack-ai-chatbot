from fastapi import FastAPI
from routes import chat                 # ✅ import your chat router
from socket.utils import create_token   # ✅ import token generator

app = FastAPI()

# ✅ include WebSocket chat routes
app.include_router(chat.router)

# ✅ token endpoint for clients
@app.get("/token")
def get_token():
    """Generate and return a new chat session token."""
    return {"token": create_token()}
