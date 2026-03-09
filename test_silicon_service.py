
import asyncio
import os
from dotenv import load_dotenv
import sys

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.app.services.silicon_flow import SiliconFlowService

async def test_service():
    load_dotenv(dotenv_path='backend/.env')
    service = SiliconFlowService()
    print("Testing SiliconFlowService.generate_image method access...")
    
    # We don't want to actually generate an image to save quota, 
    # but we want to see if the method is callable and starts the process.
    # We'll check if it prints the "🚀 Sending request" line.
    try:
        # Using a very short steps to fail fast or just check the call
        result = await service.generate_image(prompt="test", steps=1)
        print(f"Result: {result}")
    except RuntimeError as e:
        print(f"❌ RuntimeError (likely missing API key): {e}")
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")
    except Exception as e:
        print(f"Captured expected or other error: {e}")

if __name__ == "__main__":
    asyncio.run(test_service())
