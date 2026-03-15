from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.ollama import Ollama
from textwrap import dedent
from src.core.config import settings
from src.schemas.spark import AnalysisResponse
from src.integrations.file_tools import read_local_file

def get_llm_model():
    if settings.MODEL_PROVIDER == "openai":
        return OpenAIChat(
            id=settings.OPENAI_MODEL_ID, 
            api_key=settings.OPENAI_API_KEY
        )
    elif settings.MODEL_PROVIDER == "ollama":
        return Ollama(
            id=settings.OLLAMA_MODEL_ID,
            host=settings.OLLAMA_BASE_URL
        )
    else:
        raise ValueError(f"Unsupported model provider: {settings.MODEL_PROVIDER}")

def get_spark_analyzer_agent() -> Agent:
    return Agent(
        name="SparkAnalyzerAgent",
        model=get_llm_model(),
        instructions=dedent("""
            You are a Spark 3.5.4 Performance Tuning Specialist.
            Your task is to analyze Spark History Server (SHS) metrics, SQL Physical Plans, and executor metrics.
            You must identify Data Skew, Spill-to-Disk events, and suboptimal joins (e.g., missing BroadcastHashJoin or dangerous CartesianProducts).
            
            Always prioritize Static Resource Allocation over Dynamic Allocation.
        """),
        response_model=AnalysisResponse
    )

def get_airflow_analyzer_agent() -> Agent:
    return Agent(
        name="AirflowAnalyzerAgent",
        model=get_llm_model(),
        tools=[read_local_file],
        instructions=dedent("""
            You are an Airflow 3.1.7 Orchestration Specialist.
            Your task is to analyze Airflow DAG code and task logs. 
            You can use the 'read_local_file' tool to fetch the DAG code if a path is provided.
            You must identify legacy patterns (e.g., PythonOperator without TaskFlow), missing Dataset triggers, and missing Dynamic Task Mapping (.expand).
        """),
        response_model=AnalysisResponse
    )

def get_code_auditor_agent() -> Agent:
    return Agent(
        name="CodeAuditorAgent",
        model=get_llm_model(),
        tools=[read_local_file],
        instructions=dedent("""
            You are a Data Engineering Code Auditor.
            Your task is to analyze raw Python/Scala code for Apache Spark.
            You can use the 'read_local_file' tool to fetch the application code if a path is provided.
            Identify algorithmic inefficiencies, missing partitioning strategies, or poorly structured UDFs.
        """),
        response_model=AnalysisResponse
    )

