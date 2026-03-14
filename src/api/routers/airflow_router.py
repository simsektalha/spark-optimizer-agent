from fastapi import APIRouter, Depends
from src.schemas.airflow import AirflowDagPayload, AirflowTaskLogPayload
from src.schemas.spark import AnalysisResponse
from src.services.airflow_service import AirflowAnalyzerService

router = APIRouter(prefix="/airflow", tags=["Airflow Analysis"])

def get_airflow_service():
    return AirflowAnalyzerService()

@router.post("/analyze-dag", response_model=AnalysisResponse)
async def analyze_airflow_dag(
    payload: AirflowDagPayload,
    service: AirflowAnalyzerService = Depends(get_airflow_service)
):
    """
    Ingest Airflow DAG code to validate against Airflow 3.1.7 best practices
    (TaskFlow API, Metastore load reduction).
    """
    return service.analyze_dag(payload)

@router.post("/analyze-log", response_model=AnalysisResponse)
async def analyze_airflow_log(
    payload: AirflowTaskLogPayload,
    service: AirflowAnalyzerService = Depends(get_airflow_service)
):
    """
    Analyze specific Airflow task logs for failures or bottlenecks.
    """
    return service.analyze_task_log(payload)
