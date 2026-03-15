from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.agents.architect_agent import AgenticArchitect
from src.schemas.spark import AnalysisResponse

router = APIRouter(prefix="/agent", tags=["Agentic Architect"])

class AgentAnalysisRequest(BaseModel):
    app_id: str
    observed_bottleneck: str = "Unspecified bottleneck"

class FullPipelineRequest(BaseModel):
    app_id: str
    airflow_dag_code: str = ""
    spark_app_code: str = ""

@router.post("/analyze-app")
async def analyze_spark_app_agentic(request: AgentAnalysisRequest):
    """
    Triggers the Agentic Architect to perform a deep-dive investigation
    into a specific Spark application bottleneck.
    """
    agent = AgenticArchitect()
    report = await agent.analyze_bottleneck(request.app_id, request.observed_bottleneck)
    return {"app_id": request.app_id, "analysis_report": report}

@router.post("/analyze-pipeline", response_model=AnalysisResponse)
async def analyze_full_pipeline_agentic(request: FullPipelineRequest):
    """
    Triggers the Master Orchestrator to perform an end-to-end analysis
    using specialized sub-agents for Spark Metrics, Airflow DAG, and Spark Code.
    """
    agent = AgenticArchitect()
    # In a real scenario, we would fetch the raw SHS payload using SparkHistoryClient here
    # For now, we pass the app_id to the spark agent
    spark_payload = f"App ID: {request.app_id}"
    
    report = agent.analyze_full_pipeline(
        spark_payload=spark_payload,
        airflow_code=request.airflow_dag_code,
        spark_code=request.spark_app_code
    )
    return report

