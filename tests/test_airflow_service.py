import unittest
from src.services.airflow_service import AirflowAnalyzerService
from src.schemas.airflow import AirflowDagPayload

class TestAirflowAnalyzerService(unittest.TestCase):
    def setUp(self):
        self.service = AirflowAnalyzerService()

    def test_dataset_scheduling_suggestion(self):
        code = """
        dag = DAG(
            'test_dag',
            schedule='0 0 * * *',
            start_date=datetime(2023, 1, 1)
        )
        sensor = ExternalTaskSensor(task_id='wait', external_dag_id='upstream')
        """
        payload = AirflowDagPayload(dag_id="test_dag", dag_code=code)
        results = self.service.analyze_dag(payload)
        self.assertTrue(any("Dataset-based scheduling" in s for s in results.optimized_solutions))

    def test_dynamic_task_mapping_suggestion(self):
        code = """
        for i in range(10):
            PythonOperator(task_id=f'task_{i}', python_callable=my_func)
        """
        payload = AirflowDagPayload(dag_id="test_dag", dag_code=code)
        results = self.service.analyze_dag(payload)
        self.assertTrue(any("Dynamic Task Mapping" in s for s in results.optimized_solutions))

if __name__ == "__main__":
    unittest.main()
