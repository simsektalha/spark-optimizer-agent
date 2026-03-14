from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.agents.architect_agent import AgenticArchitect

router = APIRouter(prefix="/agent", tags=["Agentic Architect"])

class AgentAnalysisRequest(BaseModel):
    app_id: str
    observed_bottleneck: str = "Unspecified bottleneck"

@router.post("/analyze-app")
async def analyze_spark_app_agentic(request: AgentAnalysisRequest):
    """
    Triggers the Agentic Architect to perform a deep-dive investigation
    into a specific Spark application bottleneck.
    """
    agent = AgenticArchitect()
    report = await agent.analyze_bottleneck(request.app_id, request.observed_bottleneck)
    return {"app_id": request.app_id, "analysis_report": report}
