from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict
import uuid
from ..agent.graph import app as agent_app
from ..agent.state import AgentState

router = APIRouter()

# In-memory storage for task results (replace with Redis/DB in production)
tasks: Dict[str, Dict] = {}
import asyncio
# simple lock to avoid races when running concurrent requests
tasks_lock = asyncio.Lock()

class GenerateRequest(BaseModel):
    prompt: str
    max_iterations: int = 3
    enable_monitoring: bool = True

class FeedbackRequest(BaseModel):
    task_id: str
    rating: float
    comment: Optional[str] = None

async def run_agent_task(task_id: str, prompt: str, max_iterations: int = 3):
    async with tasks_lock:
        tasks[task_id]["status"] = "processing"
    try:
        initial_state = AgentState(
            original_prompt=prompt,
            optimized_prompt=None,
            generated_image_url=None,
            critique=None,
            iteration_count=0,
            quality_score=0.0,
            status="started",
            messages=[],
            max_iterations=max_iterations
        )
        
        # Invoke LangGraph workflow; this returns the final state dict
        final_state = await agent_app.ainvoke(initial_state)
        
        # Determine final status in case one of the nodes marked failure
        result_status = final_state.get("status", "completed")
        async with tasks_lock:
            if result_status != "completed":
                tasks[task_id].update({
                    "status": "failed",
                    "result": final_state,
                    "error": f"Agent workflow finished with status '{result_status}'"
                })
            else:
                tasks[task_id].update({
                    "status": "completed",
                    "result": final_state,
                    "error": None
                })
    except Exception as e:
        async with tasks_lock:
            tasks[task_id].update({
                "status": "failed",
                "error": str(e)
            })

@router.post("/generate")
async def generate_image(request: GenerateRequest, background_tasks: BackgroundTasks):
    # simple validation
    if not request.prompt or not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    task_id = str(uuid.uuid4())
    async with tasks_lock:
        tasks[task_id] = {
            "id": task_id,
            "status": "accepted",
            "prompt": request.prompt
        }

    background_tasks.add_task(run_agent_task, task_id, request.prompt, request.max_iterations)
    
    return {
        "task_id": task_id,
        "status": "accepted",
        "message": "Image generation started"
    }

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    response = {
        "task_id": task_id,
        "status": task["status"],
    }
    
    if task["status"] == "completed":
        result = task["result"]
        response.update({
            "generated_image": result.get("generated_image_url"),
            "quality_score": result.get("quality_score"),
            "current_step": "done"
        })
    elif task["status"] == "failed":
        response["error"] = task.get("error")
        
    return response


@router.get("/health")
async def health_check():
    """Simple health endpoint for uptime checks."""
    return {"status": "ok"}

@router.post("/feedback")
async def submit_feedback(request: FeedbackRequest):
    if request.task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Store feedback (mock implementation)
    tasks[request.task_id]["feedback"] = {
        "rating": request.rating,
        "comment": request.comment
    }
    
    return {"status": "success", "message": "Feedback received"}
