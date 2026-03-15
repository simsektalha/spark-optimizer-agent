from typing import Dict, Any, List
from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

from src.core.config import settings
from src.agents.specialists import get_llm_model, get_spark_analyzer_agent, get_airflow_analyzer_agent, get_code_auditor_agent
from src.schemas.spark import AnalysisResponse

# --- MASTER ORCHESTRATOR ---
class AgenticArchitect:
    def __init__(self):
        self.db = SqliteDb(db_file=settings.AGENT_MEMORY_DB_PATH)
        self.memory_manager = MemoryManager(db=self.db)
        
        self.spark_agent = get_spark_analyzer_agent()
        self.airflow_agent = get_airflow_analyzer_agent()
        self.code_agent = get_code_auditor_agent()

        self.system_prompt = dedent("""
            ROLE DEFINITION
            You are the Master Orchestrator: a Lead Data Solutions Architect. 
            Your job is to synthesize reports from your specialized sub-agents into a final, unified executive summary.
            
            You will be provided with analyses from:
            1. Spark Performance Agent
            2. Airflow Orchestration Agent
            3. Code Auditor Agent
            
            Synthesize these findings and provide a final JSON response matching the AnalysisResponse structure:
            - bottleneck_summary
            - current_situation
            - proposed_changes
            - goal_expectation
            
            Do not include markdown formatting, just pure JSON or the structured Pydantic format.
        """)
        
        self.agent = Agent(
            name="MasterArchitect",
            model=get_llm_model(),
            instructions=self.system_prompt,
            db=self.db,
            memory_manager=self.memory_manager,
            add_history_to_context=True,
            num_history_runs=5,
            response_model=AnalysisResponse,
            markdown=False,
            debug_mode=False
        )

    def analyze_full_pipeline(self, spark_payload: str, airflow_code: str, spark_code: str, user_id: str = "default_user") -> AnalysisResponse:
        """
        Runs the full multi-agent collective.
        """
        # 1. Delegate to specialists
        spark_analysis = self.spark_agent.run(f"Analyze this Spark data:\n{spark_payload}").content
        airflow_analysis = self.airflow_agent.run(f"Analyze this DAG:\n{airflow_code}").content
        code_analysis = self.code_agent.run(f"Analyze this Spark application code:\n{spark_code}").content
        
        # 2. Master Synthesis
        synthesis_query = f"""
        Please synthesize the following specialized reports into one final architectural summary.
        
        --- SPARK REPORT ---
        {spark_analysis}
        
        --- AIRFLOW REPORT ---
        {airflow_analysis}
        
        --- CODE AUDIT REPORT ---
        {code_analysis}
        """
        
        response = self.agent.run(synthesis_query, user_id=user_id)
        return response.content

