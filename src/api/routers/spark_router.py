from fastapi import APIRouter, Depends
from src.schemas.spark import SparkAppPayload, AnalysisResponse
from src.services.spark_service import SparkAnalyzerService

router = APIRouter(prefix="/spark", tags=["Spark Analysis"])

def get_spark_service():
    return SparkAnalyzerService()

@router.post("/analyze-app", response_model=AnalysisResponse)
async def analyze_spark_application(
    payload: SparkAppPayload,
    service: SparkAnalyzerService = Depends(get_spark_service)
):
    """
    Ingest Spark Application history payload and analyze for performance,
    skew, and configuration bottlenecks (YARN / 3.5.4 optimized).
    """
    return service.analyze_application(payload)
