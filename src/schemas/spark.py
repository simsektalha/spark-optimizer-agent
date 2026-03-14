from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SparkTaskMetrics(BaseModel):
    task_id: str
    duration_ms: int
    shuffle_read_bytes: int
    shuffle_write_bytes: int
    executor_id: str
    memory_bytes_spilled: int = 0
    disk_bytes_spilled: int = 0

class SparkStageMetrics(BaseModel):
    stage_id: int
    num_tasks: int
    tasks: List[SparkTaskMetrics]

class SparkAppPayload(BaseModel):
    app_id: str
    spark_version: str = "3.5.4"
    configuration: Dict[str, str]
    stages: List[SparkStageMetrics]
    logs: Optional[str] = None

class AnalysisResponse(BaseModel):
    layer: str
    bottlenecks: List[str]
    optimized_solutions: List[str]
    architectural_notes: List[str]
