from src.schemas.airflow import AirflowDagPayload, AirflowTaskLogPayload
from src.schemas.spark import AnalysisResponse
from src.core.config import settings

class AirflowAnalyzerService:
    def analyze_dag(self, payload: AirflowDagPayload) -> AnalysisResponse:
        bottlenecks = []
        solutions = []
        notes = []

        code = payload.dag_code
        
        if settings.AIRFLOW_REQUIRE_TASKFLOW and "PythonOperator" in code and "@task" not in code:
            bottlenecks.append("Legacy PythonOperator usage detected.")
            solutions.append("Refactor using Airflow 3.x TaskFlow API (@task) for cleaner context passing and implicit XComs.")
            notes.append("TaskFlow reduces DAG parsing overhead, improves atomicity, and standardizes data passing.")
            
        if "Variable.get" in code:
            bottlenecks.append("Top-level Variable.get() usage detected.")
            solutions.append("Move Variable.get() inside task execution blocks or use Jinja templating (e.g., {{ var.value.my_var }}).")
            notes.append("Top-level variable access crushes the Airflow metastore DB during the continuous DAG parsing loop.")

        # 3. Dataset-based Scheduling (Modern Airflow 3.1.7)
        if "schedule=" in code and "Dataset" not in code and ("trigger" in code or "ExternalTaskSensor" in code):
            bottlenecks.append("Traditional cron/sensor-based dependency found instead of Dataset triggers.")
            solutions.append("Refactor to Dataset-based scheduling (e.g., schedule=[Dataset('s3://my-bucket/data')]).")
            notes.append("Datasets allow for event-driven DAG execution, removing the need for polling sensors which waste worker slots.")

        # 4. Dynamic Task Mapping (DTM) checks
        if "for " in code and ".expand(" not in code and ".partial(" not in code:
            if "dag" in code.lower() or "task" in code.lower():
                bottlenecks.append("Manual 'for' loop for task generation detected.")
                solutions.append("Use Airflow Dynamic Task Mapping (.expand()) for horizontal scaling.")
                notes.append("DTM allows tasks to be created dynamically at runtime based on upstream data, which is more efficient than static DAG generation.")

        return AnalysisResponse(
            layer="Orchestration (Airflow 3.1.7)",
            bottlenecks=bottlenecks,
            optimized_solutions=solutions,
            architectural_notes=notes
        )

    def analyze_task_log(self, payload: AirflowTaskLogPayload) -> AnalysisResponse:
        bottlenecks = []
        solutions = []
        
        if "Dependencies not met" in payload.log_content:
            bottlenecks.append("Task stuck in upstream dependency wait state.")
            solutions.append("Check Dataset triggers or upstream sensor configurations for missed SLAs.")
            
        return AnalysisResponse(
            layer="Orchestration (Airflow 3.1.7)",
            bottlenecks=bottlenecks,
            optimized_solutions=solutions,
            architectural_notes=["Ensure atomicity; task retries must be strictly idempotent to avoid data duplication in the data lake."]
        )
