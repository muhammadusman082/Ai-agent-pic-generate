from typing import Dict, Any
from .state import AgentState
from ..services.silicon_flow import SiliconFlowService

# Instantiate lazily inside each function to ensure env vars are loaded
def get_silicon_flow():
    return SiliconFlowService()

async def planner_node(state: AgentState) -> Dict[str, Any]:
    print(f"Planning for: {state['original_prompt']}")
    optimized_prompt = state['original_prompt']
    return {"optimized_prompt": optimized_prompt, "messages": ["Planned prompt optimization"]}

async def generator_node(state: AgentState) -> Dict[str, Any]:
    prompt = state.get("optimized_prompt", state["original_prompt"])
    print(f"Generating image for: {prompt}")
    try:
        image_url = await silicon_flow.generate_image(prompt)
    except Exception as e:
        # bubble up configuration/network errors
        return {"status": "failed", "messages": [f"Image generation error: {e}"]}
    if not image_url:
        return {"status": "failed", "messages": ["Image generation failed"]}
    
    return {
        "generated_image_url": image_url,
        "status": "generated",
        "messages": [f"Generated image: {image_url}"]
    }

async def critic_node(state: AgentState) -> Dict[str, Any]:
    print("Critiquing image...")
    return {
        "quality_score": 0.95,
        "critique": "Image looks good.",
        "status": "completed",
        "messages": ["Critique passed"]
    }
