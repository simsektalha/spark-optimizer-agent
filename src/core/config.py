from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Data Architect AI Agent"
    API_V1_STR: str = "/api/v1"
    
    # AI / LLM Configuration
    MODEL_PROVIDER: str = "openai"  # "openai" or "ollama"
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL_ID: str = "gpt-4o"
    OLLAMA_MODEL_ID: str = "llama3.1"
    OLLAMA_BASE_URL: str | None = None
    AGENT_MEMORY_DB_PATH: str = "tmp/architect_memory.db"
    
    # Spark Analysis Thresholds (Enterprise Configurable)
    SPARK_HISTORY_SERVER_URL: str = "http://localhost:18080"
    SPARK_SKEW_THRESHOLD_MULTIPLIER: float = 3.0
    SPARK_MEMORY_OVERHEAD_WARNING_PERCENT: float = 0.85
    
    # Airflow Rules
    AIRFLOW_REQUIRE_TASKFLOW: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
