from src.schemas.spark import SparkAppPayload, AnalysisResponse
from src.agents.specialists import get_spark_analyzer_agent
import json

class SparkAnalyzerService:
    def __init__(self):
        self.agent = get_spark_analyzer_agent()

    def analyze_application(self, payload: SparkAppPayload) -> AnalysisResponse:
        input_query = f"Analyze these Spark {payload.spark_version} metrics and logs:\n\n"
        input_query += f"Configuration: {json.dumps(payload.configuration)}\n"
        input_query += f"Stages/Tasks: {payload.model_dump_json(include={'stages'})}\n"
        
        if payload.logs:
            input_query += f"Logs/Execution Plan: {payload.logs}\n"
            
        response = self.agent.run(input_query)
        return response.content
