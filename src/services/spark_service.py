from src.schemas.spark import SparkAppPayload, AnalysisResponse
from src.core.config import settings

class SparkAnalyzerService:
    def analyze_application(self, payload: SparkAppPayload) -> AnalysisResponse:
        bottlenecks = []
        solutions = []
        notes = []
        
        # 1. Configuration checks
        if payload.configuration.get("spark.dynamicAllocation.enabled") == "true":
            bottlenecks.append("Dynamic Resource Allocation is enabled.")
            solutions.append("Disable dynamic allocation. Prioritize Static Resource Allocation: set spark.executor.instances, spark.executor.cores, and spark.executor.memory manually for predictable performance.")
            notes.append("In strict YARN environments, dynamic allocation can lead to unpredictable queue starvation and resource fragmentation.")
            
        # 2. Skew Analysis
        for stage in payload.stages:
            if not stage.tasks: continue
            avg_duration = sum(t.duration_ms for t in stage.tasks) / len(stage.tasks)
            max_duration = max(t.duration_ms for t in stage.tasks)
            
            if max_duration > (avg_duration * settings.SPARK_SKEW_THRESHOLD_MULTIPLIER):
                bottlenecks.append(f"Stage {stage.stage_id} exhibits severe task duration skew (Max {max_duration}ms vs Avg {avg_duration}ms).")
                solutions.append("Implement manual salting or enable AQE Skew Join optimization (spark.sql.adaptive.skewJoin.enabled=true).")
                notes.append("Shuffle skew drastically underutilizes YARN container resources while one executor grinds. Consider Iceberg hidden partitioning if skew originates from source storage.")
                break # Report once per app for brevity
                
        # 3. Log Analysis (if provided)
        if payload.logs and "Physical memory usage" in payload.logs:
            bottlenecks.append("YARN container killed due to physical memory limits.")
            solutions.append("Increase spark.executor.memoryOverhead (default is 10% or 384MB). Adjust spark.memory.fraction if Tungsten is caching too heavily.")

        # 4. Spill-to-Disk Analysis (Deep Metric Correlation)
        for stage in payload.stages:
            stage_mem_spill = sum(t.memory_bytes_spilled for t in stage.tasks)
            stage_disk_spill = sum(t.disk_bytes_spilled for t in stage.tasks)
            
            if stage_disk_spill > 0:
                bottlenecks.append(f"Stage {stage.stage_id} triggered Spill-to-Disk ({stage_disk_spill / 1024**2:.2f} MB).")
                solutions.append("Increase spark.executor.memory or spark.memory.fraction. Consider increasing spark.sql.shuffle.partitions to reduce per-task data volume.")
                notes.append("Spill-to-disk significantly degrades performance as it replaces fast memory access with slow disk I/O, often leading to executor OOM.")
                break

        # 5. SQL Physical Plan Parsing (Logical Layer Analysis)
        # Note: In a full implementation, we'd pass the physical plan from SHS here
        # This is a pattern-matching demonstration on the 'logs' or a dedicated field
        if payload.logs:
            if "SortMergeJoin" in payload.logs and "BroadcastHashJoin" not in payload.logs:
                # Suggest broadcast if we suspect small tables (heuristic)
                notes.append("SortMergeJoin detected. Ensure tables are properly bucketed or verify if one side can be broadcasted via spark.sql.autoBroadcastJoinThreshold.")
            
            if "CartesianProduct" in payload.logs:
                bottlenecks.append("CartesianProduct join detected in execution plan.")
                solutions.append("Explicitly rewrite join condition to avoid CROSS JOIN. Check for missing join keys.")
                notes.append("Cartesian products lead to exponential growth in row counts, usually crashing executors in production.")

        if not bottlenecks:
            notes.append("Application appears to be running within acceptable parameters.")

        return AnalysisResponse(
            layer="Compute (Spark 3.5.4 / YARN)",
            bottlenecks=bottlenecks,
            optimized_solutions=solutions,
            architectural_notes=notes
        )
