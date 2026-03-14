import httpx
import asyncio
from typing import List, Dict, Any
from src.core.config import settings

class SparkHistoryClient:
    """
    Asynchronous client for Spark History Server (SHS) API.
    Optimized for Spark 3.5.4 REST API endpoints.
    """
    def __init__(self, base_url: str = None):
        self.base_url = (base_url or settings.SPARK_HISTORY_SERVER_URL or "http://localhost:18080").rstrip("/")
        self.timeout = httpx.Timeout(45.0, connect=10.0)

    async def get_app_details(self, app_id: str) -> Dict[str, Any]:
        """Fetch application, stages, executors, and SQL plans concurrently."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            endpoints = [
                f"{self.base_url}/api/v1/applications/{app_id}",
                f"{self.base_url}/api/v1/applications/{app_id}/stages",
                f"{self.base_url}/api/v1/applications/{app_id}/executors",
                f"{self.base_url}/api/v1/applications/{app_id}/sql"
            ]
            responses = await asyncio.gather(*(client.get(url) for url in endpoints))
            
            # Application metadata might 404 if not found, but we want to be safe
            for r in responses:
                r.raise_for_status()
                
            app, stages, executors, sql = [r.json() for r in responses]
            return {
                "app_id": app_id,
                "metadata": app,
                "stages": stages,
                "executors": executors,
                "sql": sql
            }

    async def get_sql_details(self, app_id: str, sql_id: int) -> Dict[str, Any]:
        """Fetch detailed physical plan for a specific SQL execution."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            url = f"{self.base_url}/api/v1/applications/{app_id}/sql/{sql_id}"
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def get_fleet_metrics(self, app_ids: List[str], concurrency: int = 10) -> List[Dict[str, Any]]:
        """Fetch metrics for 70+ apps using a semaphore to protect SHS from OOM."""
        semaphore = asyncio.Semaphore(concurrency)
        
        async def fetch_with_sem(app_id: str):
            async with semaphore:
                return await self.get_app_details(app_id)
                
        return await asyncio.gather(*(fetch_with_sem(aid) for aid in app_ids))
