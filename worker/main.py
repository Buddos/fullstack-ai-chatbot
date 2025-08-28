import asyncio
import os
import aiohttp
from dotenv import load_dotenv
from src.redis.config import get_redis_pool

load_dotenv()

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"

async def call_huggingface(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(HUGGINGFACE_API_URL, headers=headers, json={"inputs": prompt}) as response:
            if response.status == 200:
                result = await response.json()
                return result[0]["generated_text"]
            else:
                return f"Error: {response.status}"

async def main():
    redis = await get_redis_pool()
    print("✅ Connected to Redis")

    pubsub = redis.pubsub()
    await pubsub.subscribe("chat_channel")

    async for message in pubsub.listen():
        if message["type"] == "message":
            prompt = message["data"]
            print(f"📩 Received: {prompt}")

            response = await call_huggingface(prompt)
            print(f"🤖 HuggingFace Response: {response}")

            await redis.set("last_response", response)

if __name__ == "__main__":
    asyncio.run(main())
