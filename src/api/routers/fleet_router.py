from fastapi import APIRouter, Depends, Query
from typing import List
from src.schemas.spark import AnalysisResponse
from src.integrations.spark_history import SparkHistoryClient
from src.services.spark_service import SparkAnalyzerService
from src.schemas.spark import SparkAppPayload, SparkStageMetrics, SparkTaskMetrics

router = APIRouter(prefix="/fleet", tags=["Fleet Analysis"])

@router.post("/analyze-ids", response_model=List[AnalysisResponse])
async def analyze_fleet_by_ids(
    app_ids: List[str],
    history_client: SparkHistoryClient = Depends(lambda: SparkHistoryClient()),
    analyzer: SparkAnalyzerService = Depends(lambda: SparkAnalyzerService())
):
    """
    Batch analyze 70+ application IDs by pulling data from Spark History Server API.
    """
    raw_fleet_data = await history_client.get_fleet_metrics(app_ids)
    
    analysis_results = []
    for app in raw_fleet_data:
        # Transform raw SHS JSON to our validated SparkAppPayload
        stages_payload = []
        for s in app["stages"]:
            stages_payload.append(SparkStageMetrics(
                stage_id=s["stageId"],
                num_tasks=s["numTasks"],
                tasks=[] # Detail tasks could be added here if needed
            ))
            
        payload = SparkAppPayload(
            app_id=app["app_id"],
            configuration={}, # Could pull from environment/defaults
            stages=stages_payload
        )
        analysis_results.append(analyzer.analyze_application(payload))
        
    return analysis_results
