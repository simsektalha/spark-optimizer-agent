from src.schemas.airflow import AirflowDagPayload, AirflowTaskLogPayload
from src.schemas.spark import AnalysisResponse
from src.agents.specialists import get_airflow_analyzer_agent

class AirflowAnalyzerService:
    def __init__(self):
        self.agent = get_airflow_analyzer_agent()

    def analyze_dag(self, payload: AirflowDagPayload) -> AnalysisResponse:
        input_query = f"Analyze this Airflow DAG code for version {payload.airflow_version}:\n\n{payload.dag_code}"
        
        response = self.agent.run(input_query)
        return response.content

    def analyze_task_log(self, payload: AirflowTaskLogPayload) -> AnalysisResponse:
        input_query = f"Analyze this task log for DAG '{payload.dag_id}' task '{payload.task_id}':\n\n{payload.log_content}"
        
        response = self.agent.run(input_query)
        return response.content
