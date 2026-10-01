import time
import json
import re
from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field, ValidationError
from crewai import Crew, Process
from agents import create_agents
from tasks import create_tasks

class JobInput(BaseModel):
    description: str = Field(..., min_length=10, max_length=4000)
    name: str = "Alex"
    rate: float = 50.0
    skills: str = ""
    availability: str = ""
    experience: str = ""
    tone: str = "professional"

class DashboardMetrics(BaseModel):
    fit_score_1_to_10: int = 0
    decision: str = "UNKNOWN"
    estimated_hours: int = 0
    recommended_price_usd: int = 0

def extract_json_metrics(text: str) -> DashboardMetrics:
    try:
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
        if match:
            data = json.loads(match.group(1))
            return DashboardMetrics(**data)
    except (json.JSONDecodeError, ValidationError):
        pass
    return DashboardMetrics()

def run_crew(job_description: str, api_key: str, profile_data: dict) -> Tuple[bool, str, Dict[str, Any]]:
    try:
        valid_input = JobInput(
            description=job_description, 
            name=profile_data.get('name', 'Alex'),
            rate=profile_data.get('rate', 50.0),
            skills=profile_data.get('skills', ''),
            availability=profile_data.get('availability', ''),
            experience=profile_data.get('experience', ''),
            tone=profile_data.get('tone', 'professional')
        )
    except ValidationError as e:
        return False, "Input validation failed: Please ensure the job description is between 10 and 4000 characters.", {}

    # Updated to Gemini 3.5 models
    models_to_try = ["gemini/gemini-3.5-flash", "gemini/gemini-3.5-flash-lite"]
    
    for attempt, model in enumerate(models_to_try):
        try:
            agents = create_agents(api_key, model)
            tasks = create_tasks(agents, valid_input)
            
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                max_rpm=8,
                verbose=False
            )
            
            crew_output = crew.kickoff()
            
            task_outputs = {
                "lead_analysis": tasks[0].output.raw if tasks[0].output else "No output",
                "proposal": tasks[1].output.raw if tasks[1].output else "No output",
                "project_plan": tasks[2].output.raw if tasks[2].output else "No output",
                "finance": tasks[3].output.raw if tasks[3].output else "No output",
            }
            
            metrics = extract_json_metrics(task_outputs["finance"])
            task_outputs["metrics"] = metrics.dict()
            task_outputs["model_used"] = model
            
            return True, "Success", task_outputs

        except Exception as e:
            error_str = str(e)
            if api_key in error_str:
                error_str = error_str.replace(api_key, "***[REDACTED_API_KEY]***")
            
            if "429" in error_str or "ResourceExhausted" in error_str or "Quota" in error_str:
                if attempt == 0:
                    time.sleep(3) 
                    continue
                else:
                    return False, "Rate limit or Quota exceeded. Please wait or use your own API key.", {}
            
            if "API_KEY_INVALID" in error_str or "401" in error_str or "403" in error_str:
                return False, "Invalid API key provided. Please check the key and try again.", {}
            
            if attempt == 0:
                continue
            
            return False, f"An unexpected error occurred: {error_str}", {}

    return False, "All attempts failed.", {}