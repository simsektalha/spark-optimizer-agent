# Suggested Commands

## Running the Application
- **Start FastAPI Server**: `uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload`
- **Build Docker Image**: `docker build -t spark-optimizer-agent .`
- **Run Docker Container**: `docker run -p 8000:8000 --env-file .env spark-optimizer-agent`

## Testing
- **Run All Tests**: `python -m unittest discover tests`
- **Run Specific Test File**: `python -m unittest tests/test_spark_service.py`

## Git Workflow (Global Mandate)
- **Create Feature Branch**: `git checkout -b feat/your-feature-name`
- **Commit Changes**: `git commit -m "feat: description"`
- **Push and Open PR**: `git push origin feat/your-feature-name` (then open PR on GitHub)
- **Merge Rule**: PRs can be merged after at least one successful review. CRITICAL issues must be resolved and re-reviewed.

## Windows Utilities (PowerShell)
- **List Files**: `ls` or `dir`
- **Search Pattern**: `grep` (if installed) or `Select-String -Pattern "pattern" -Path "file"`
- **Remove File**: `rm` or `Remove-Item`
- **Make Directory**: `mkdir` or `New-Item -ItemType Directory`
