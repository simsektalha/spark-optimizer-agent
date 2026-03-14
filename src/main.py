from fastapi import FastAPI
from src.core.config import settings
from src.api.routers import spark_router, airflow_router, fleet_router, agent_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise API for Data Architecture & Spark/Airflow optimization. Agentic loop for deep-dive analysis.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(spark_router.router, prefix=settings.API_V1_STR)
app.include_router(airflow_router.router, prefix=settings.API_V1_STR)
app.include_router(fleet_router.router, prefix=settings.API_V1_STR)
app.include_router(agent_router.router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.1.0", "stack": "Spark 3.5.4 | Airflow 3.1.7 | Agno Agent"}
