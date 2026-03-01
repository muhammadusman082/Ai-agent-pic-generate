import os
import httpx
import logging
from typing import Optional   # ✅ YEH IMPORTANT LINE

LOGGER = logging.getLogger(__name__)

class SiliconFlowService:
    def __init__(self):
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        self.base_url = "https://api.siliconflow.cn/v1"
        print(f"🔑 API Key Loaded: {'Yes' if self.api_key else 'No'}")
        if self.api_key:
            print(f"🔑 API Key (first 10 chars): {self.api_key[:10]}...")


    async def generate_image(self, prompt: str, steps: int = 20) -> Optional[str]:
        if not self.api_key:
            # escalate the missing key since it's a configuration issue
            raise RuntimeError("SiliconFlow API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "black-forest-labs/FLUX.1-schnell",
            "prompt": prompt,
            "image_size": "1024x1024",
            "num_inference_steps": steps
        }
        
        print(f"🚀 Sending request to SiliconFlow...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/images/generations",
                    headers=headers,
                    json=payload
                )
                
                print(f"📥 Response Status: {response.status_code}")
                
                # If the request failed, log body for debugging
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as http_err:
                    print(f"❌ HTTP error from SiliconFlow: {http_err}")
                    print("Response body:", response.text)
                    return None

                data = response.json()
                
                # support both old and new response formats
                if "images" in data and len(data["images"]) > 0:
                    image_url = data["images"][0].get("url")
                    print(f"✅ Image URL (from images): {image_url}")
                    return image_url
                elif "data" in data and len(data["data"]) > 0:
                    image_url = data["data"][0].get("url")
                    print(f"✅ Image URL (from data): {image_url}")
                    return image_url
                else:
                    print(f"❌ No image URL found in response: {data}")
                    return None
                    
            except Exception as e:
                # catch network issues, timeouts, etc.
                print(f"❌ Error contacting SiliconFlow: {str(e)}")
                return None