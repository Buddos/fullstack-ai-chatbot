from fastapi import FastAPI, Request
import uvicorn
import os
from dotenv import load_dotenv
from src.routes.chat import chat   # import the chat router

# Load environment variables
load_dotenv()

# Initialize FastAPI app
api = FastAPI()

# Register the chat router
api.include_router(chat)

# Test route
@api.get("/test")
async def root():
    return {"msg": "API is Online"}

if __name__ == "__main__":
    if os.environ.get('APP_ENV') == "development":
        uvicorn.run("api:api", host="0.0.0.0", port=3500,
                    workers=4, reload=True)
    else:
        pass
