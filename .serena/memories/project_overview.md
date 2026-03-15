# Project Overview: Lead Data Architect AI Agent

## Purpose
An enterprise-grade AI Agent designed to optimize Spark 3.5.4 and Airflow 3.1.7 ecosystems. It provides automated analysis of Spark logs, SQL physical plans, and Airflow DAGs to identify bottlenecks and suggest modernization strategies (e.g., Iceberg migration, TaskFlow API, Dataset triggers).

## Tech Stack
- **Web Framework**: FastAPI (Asynchronous API)
- **Agent Framework**: [Agno](https://agno.com) (Multi-agent systems with shared memory)
- **Database / Persistence**: SQLAlchemy / SQLModel with SQLite (configured via `AGENT_MEMORY_DB_PATH`)
- **LLM Providers**: OpenAI (GPT-4o) and local inference via Ollama
- **HTTP Client**: httpx (for async REST integration with Spark History Server)
- **Containerization**: Docker (Python 3.10-slim)

## Architecture
1. **Integrations**: `SparkHistoryClient` for fetching metrics and plans from SHS.
2. **Services**: `SparkAnalyzerService` and `AirflowAnalyzerService` for heuristic-based analysis.
3. **Agents**: `AgenticArchitect` using Agno to orchestrate tools and synthesize architectural reports.
4. **Schemas**: Pydantic models for request/response validation.
5. **API**: FastAPI routers for agentic deep-dives, fleet analysis, and DAG validation.

## Key Features
- **Spark Optimization**: Physical plan parsing, spill-to-disk correlation, and shuffle skew detection.
- **Airflow Modernization**: TaskFlow API enforcement, Dataset-based scheduling, and Dynamic Task Mapping (DTM) checks.
- **Enterprise Privacy**: Support for local models (Ollama) and semaphore-protected high-concurrency fleet analysis.
