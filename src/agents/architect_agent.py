from typing import Dict, Any, List, Union
from textwrap import dedent
import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.ollama import Ollama
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

from src.integrations.spark_history import SparkHistoryClient
from src.core.config import settings

# --- AGENT TOOLS ---
# ... (rest of the tools unchanged)
async def fetch_spark_stages(app_id: str) -> List[Dict[str, Any]]:
    """Fetches all stages for a Spark app_id including duration, tasks, and failure reason."""
    client = SparkHistoryClient()
    details = await client.get_app_details(app_id)
    return details["stages"]

async def fetch_spark_executors(app_id: str) -> List[Dict[str, Any]]:
    """Fetches real-time executor status including memory usage and task distribution."""
    client = SparkHistoryClient()
    details = await client.get_app_details(app_id)
    return details["executors"]

async def fetch_spark_sql_plans(app_id: str) -> List[Dict[str, Any]]:
    """Fetches SQL execution plans for Spark SQL queries executed in this app."""
    client = SparkHistoryClient()
    details = await client.get_app_details(app_id)
    sql_executions = details.get("sql", [])
    
    plans = []
    # For performance, only fetch details for the last 3 SQL executions
    for sql in sql_executions[-3:]:
        sql_id = sql.get("id")
        if sql_id is not None:
            full_detail = await client.get_sql_details(app_id, sql_id)
            plans.append({
                "sql_id": sql_id,
                "description": sql.get("description"),
                "physical_plan": full_detail.get("physicalPlanDescription")
            })
    return plans

# --- AGENT CORE ---
class AgenticArchitect:
    def __init__(self, model_name: str | None = None):
        self.db = SqliteDb(db_file="tmp/architect_memory.db")
        self.memory_manager = MemoryManager(db=self.db)
        
        # 1. Initialize Model based on Provider Configuration
        if settings.MODEL_PROVIDER == "openai":
            self.model = OpenAIChat(
                id=model_name or settings.OPENAI_MODEL_ID, 
                api_key=settings.OPENAI_API_KEY
            )
        elif settings.MODEL_PROVIDER == "ollama":
            self.model = Ollama(
                id=model_name or settings.OLLAMA_MODEL_ID,
                host=settings.OLLAMA_BASE_URL
            )
        else:
            raise ValueError(f"Unsupported model provider: {settings.MODEL_PROVIDER}")

        self.system_prompt = dedent("""
            ROLE DEFINITION
            You are a Lead Data Solutions Architect and Senior AI Engineer specialized in Spark 3.5.4, Airflow 3.1.7, and Python 3.8+. 
            Your core mission is to analyze, optimize, and scale complex data pipelines within a YARN-managed HDFS environment. 
            You act as a strategic engineering partner who prioritizes performance, resource efficiency, and structural integrity.

            TECHNICAL DOMAINS & CONSTRAINTS
            - Spark 3.5.4 & YARN Optimization: Focus on skewness mitigation, shuffle tuning, and memory management.
            - CRITICAL CONSTRAINT: Prioritize static resource allocation. Do not suggest Dynamic Resource Allocation unless explicitly requested.
            - Airflow 3.1.7 Orchestration: TaskFlow API, Dynamic Task Mapping, Dataset-based scheduling.
            - Data Lakehouse Evolution (Iceberg): Treat Iceberg as a tool for optimization (ACID, Partition Evolution).

            OPERATIONAL PROTOCOL
            1. Root Cause Analysis: Architectural decomposition (Compute/Orchestration/Storage).
            2. Performance-First Implementation: Explain performance implications.
            3. Refactoring & Modernization: Subtly suggest Iceberg improvements.
            4. No External Dependencies: Spark, Airflow, HDFS, Iceberg, Python.

            REQUIRED RESPONSE STRUCTURE
            ### [Technical Analysis]
            - A concise breakdown of the engineering challenge.
            - Identification of the bottleneck layer.

            ### [Optimized Solution]
            - High-quality, type-hinted Python code or Spark/Airflow configuration blocks.

            ### [Architectural Notes]
            - Critical warnings regarding resource consumption, data skew, or maintenance requirements.
            - Performance implications of the chosen approach.
        """)
        
        self.agent = Agent(
            name="ArchitectAgent",
            model=self.model,
            tools=[fetch_spark_stages, fetch_spark_executors, fetch_spark_sql_plans],
            instructions=self.system_prompt,
            db=self.db,
            memory_manager=self.memory_manager,
            add_history_to_context=True,
            num_history_runs=5,
            markdown=True,
            debug_mode=False
        )

    async def analyze_bottleneck(self, app_id: str, context: str = "", user_id: str = "default_user") -> str:
        """
        Runs the agentic loop using Agno to investigate a specific Spark bottleneck.
        """
        input_query = f"Investigate Spark Application {app_id}. Observed bottleneck: {context}. Gather stages, executors, and plans to provide a solution."
        
        # Agno's run method can be async if the model supports it or if using AsyncAgent
        # For now, we'll use the standard run and wrap it if needed, 
        # but Agno also supports async natively in some versions.
        response = self.agent.run(input_query, user_id=user_id)
        return response.content
