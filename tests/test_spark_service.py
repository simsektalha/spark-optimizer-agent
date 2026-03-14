import unittest
from src.services.spark_service import SparkAnalyzerService
from src.schemas.spark import SparkAppPayload, SparkStageMetrics, SparkTaskMetrics

class TestSparkAnalyzerService(unittest.TestCase):
    def setUp(self):
        self.service = SparkAnalyzerService()

    def test_spill_to_disk_detection(self):
        task = SparkTaskMetrics(
            task_id="0", duration_ms=1000, 
            shuffle_read_bytes=0, shuffle_write_bytes=0, 
            executor_id="1", memory_bytes_spilled=100, 
            disk_bytes_spilled=1048576 # 1 MB
        )
        stage = SparkStageMetrics(stage_id=0, num_tasks=1, tasks=[task])
        payload = SparkAppPayload(app_id="test", configuration={}, stages=[stage])
        
        results = self.service.analyze_application(payload)
        self.assertTrue(any("Spill-to-Disk" in b for b in results.bottlenecks))

    def test_cartesian_product_detection(self):
        payload = SparkAppPayload(
            app_id="test", configuration={}, stages=[], 
            logs="Physical Plan: CartesianProduct Join id=1"
        )
        results = self.service.analyze_application(payload)
        self.assertTrue(any("CartesianProduct" in b for b in results.bottlenecks))

if __name__ == "__main__":
    unittest.main()
