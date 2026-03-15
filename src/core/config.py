from typing import Any, Tuple, Type
import yaml
from pathlib import Path
from pydantic_settings import (
    BaseSettings, 
    PydanticBaseSettingsSource, 
    SettingsConfigDict
)

class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a YAML file.
    """
    def __init__(self, settings_cls: Type[BaseSettings]):
        super().__init__(settings_cls)
        self.config_path = Path("config/settings.yaml")

    def get_dict_content(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r") as f:
            return yaml.safe_load(f) or {}

    def __call__(self) -> dict[str, Any]:
        return self.get_dict_content()

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str
    API_V1_STR: str
    
    # AI / LLM Configuration (Values from ENV/YAML)
    MODEL_PROVIDER: str = "openai"  # Default if not in YAML/ENV
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL_ID: str
    OLLAMA_MODEL_ID: str
    OLLAMA_BASE_URL: str | None
    
    # Agent Memory
    AGENT_MEMORY_DB_PATH: str
    
    # Spark Analysis Thresholds
    SPARK_HISTORY_SERVER_URL: str
    SPARK_SKEW_THRESHOLD_MULTIPLIER: float
    SPARK_MEMORY_OVERHEAD_WARNING_PERCENT: float
    
    # Airflow Rules
    AIRFLOW_REQUIRE_TASKFLOW: bool
    
    # Configuration Priority: ENV VARS > .env file > YAML file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return init_settings, env_settings, dotenv_settings, YamlConfigSettingsSource(settings_cls)

settings = Settings()
