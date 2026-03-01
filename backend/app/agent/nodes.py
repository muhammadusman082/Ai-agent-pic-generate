from typing import Dict, Any
from .state import AgentState
from ..services.silicon_flow import SiliconFlowService

silicon_flow = SiliconFlowService()

async def planner_node(state: AgentState) -> Dict[str, Any]:
    # In a real scenario, we might use an LLM here to optimize the prompt.
    # For now, we will just pass through or slightly modify.
    print(f"Planning for: {state['original_prompt']}")
    optimized_prompt = state['original_prompt'] # Placeholder for LLM optimization
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
    # Placeholder for critique logic
    # In reality, this would use a VLM (Vision Language Model) to check the image.
    print("Critiquing image...")
    # For now, we just approve everything to keep it simple
    return {
        "quality_score": 0.95,
        "critique": "Image looks good.",
        "status": "completed",
        "messages": ["Critique passed"]
    }
