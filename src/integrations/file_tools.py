import aiofiles
import os

async def read_local_file(file_path: str) -> str:
    """
    Reads the content of a local file. Useful for reading DAG code or Spark application code.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        async with aiofiles.open(file_path, mode='r') as f:
            return await f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"
