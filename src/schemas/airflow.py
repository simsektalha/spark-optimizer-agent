from pydantic import BaseModel
from typing import List, Optional
from src.schemas.spark import AnalysisResponse

class AirflowDagPayload(BaseModel):
    dag_id: str
    airflow_version: str = "3.1.7"
    dag_code: str

class AirflowTaskLogPayload(BaseModel):
    dag_id: str
    task_id: str
    execution_date: str
    log_content: str
