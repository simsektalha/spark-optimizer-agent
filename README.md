# 📋 Lead Data Architect AI Agent

An enterprise-grade, agentic solution for optimizing **Spark 3.5.4** and **Airflow 3.1.7** ecosystems. This agent acts as a **Lead Data Solutions Architect**, providing deep-dive analysis into performance bottlenecks, execution plans, and orchestration patterns within YARN-managed HDFS environments.

---

## 🚀 Key Features

### ⚡ Deep Spark 3.5.4 Analysis
- **Physical Plan Parsing**: Identifies suboptimal join strategies (e.g., `SortMergeJoin` vs. `BroadcastHashJoin`) and high-risk patterns like `CartesianProduct`.
- **Spill-to-Disk Correlation**: Detects `diskBytesSpilled` at the task and stage level to identify memory overhead violations.
- **Skew Mitigation**: Heuristic detection of severe task duration skew with specific recommendations for AQE or manual salting.

### 🔄 Airflow 3.1.7 Modernization
- **TaskFlow API Validation**: Automatically suggests refactoring legacy `PythonOperator` to `@task` decorators.
- **Dataset-based Scheduling**: Identifies polling sensors and suggests migration to event-driven Dataset triggers to free up worker slots.
- **Dynamic Task Mapping (DTM)**: Detects manual task-generation loops and suggests `.expand()` for horizontal scalability.

### 🧠 Agentic Intelligence (Powered by Agno)
- **Stateful Persistence**: Uses Agno's `MemoryManager` and `SqliteDb` to maintain context across multi-turn architectural deep-dives.
- **Tool-Calling Architecture**: The agent autonomously fetches stages, executors, and physical plans from the **Spark History Server (SHS)** API to ground its recommendations in real execution data.

### 🛡️ Enterprise Privacy & Flexibility
- **Multi-Model Support**: Seamlessly toggle between **OpenAI (GPT-4o)** and local inference engines like **Ollama (Llama 3)** for data-sensitive environments.
- **Fleet Analysis**: Built-in concurrency control (semaphore-protected) to safely analyze 70+ application IDs simultaneously without overwhelming the SHS.

---

## 🛠️ Tech Stack

- **Framework**: [Agno](https://agno.com) (Multi-agent systems)
- **API Layer**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous endpoints)
- **Inference**: OpenAI / Ollama
- **Persistence**: SQLAlchemy / SQLModel (Sqlite/Postgres)
- **Integration**: httpx (Async REST for Spark History Server)
- **Containerization**: Docker (Python 3.10-slim)

---

## 🏁 Getting Started

### 1. Installation
```bash
git clone https://github.com/simsektalha/data-architect-agent-repository.git
cd data-architect-agent-repository
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
MODEL_PROVIDER=openai # or ollama
OPENAI_API_KEY=your_key_here
SPARK_HISTORY_SERVER_URL=http://localhost:18080
OLLAMA_BASE_URL=http://localhost:11434 # if using ollama
```

### 3. Run with Docker
```bash
docker build -t data-architect-agent .
docker run -p 8000:8000 --env-file .env data-architect-agent
```

---

## 📊 API Usage

### Agentic Deep-Dive
Triggers the Agno agent to perform a multi-tool investigation into a specific Spark application.
```bash
POST /api/v1/agent/analyze-app
{
  "app_id": "application_123456789_0001",
  "observed_bottleneck": "Slow shuffle during stage 4"
}
```

### Batch Fleet Analysis
Analyze multiple Spark applications concurrently.
```bash
POST /api/v1/fleet/analyze-ids
["app_id_1", "app_id_2", "..."]
```

### Airflow DAG Validation
Check DAG code for 3.1.7 best practices.
```bash
POST /api/v1/airflow/analyze-dag
{
  "dag_id": "ingestion_pipeline",
  "dag_code": "..."
}
```

---

## 🏛️ Architecture Overview

The project follows a **Research -> Strategy -> Execution** pattern:
1.  **Integrations Layer**: Async clients pull raw metrics/plans from SHS.
2.  **Service Layer**: Heuristic-based `SparkAnalyzerService` and `AirflowAnalyzerService` perform initial triage.
3.  **Agentic Layer**: **Agno Agent** uses these services as tools to synthesize a high-level architectural report following the **Required Response Structure** (Technical Analysis, Optimized Solution, Architectural Notes).

---

## 📜 License
This project is for enterprise architectural optimization and follows the Lead Data Solutions Architect directives.
