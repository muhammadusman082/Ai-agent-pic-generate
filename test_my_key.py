import asyncio
import httpx

async def test():
    api_key = "sk-rlrkcscsruslahomcmyqbvyxkjoqxsiyyywyijerxlbvtjvz"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": "Test image",
        "image_size": "1024x1024",
        "num_inference_steps": 20
    }
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.siliconflow.cn/v1/images/generations", headers=headers, json=payload)
        print("Status code:", res.status_code)
        print("Response:", res.text)

asyncio.run(test())
