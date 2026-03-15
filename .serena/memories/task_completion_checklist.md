# Task Completion Checklist

Before considering a task "Finished", ensure the following:

## 1. Code Quality
- [ ] All functions have type hints and docstrings.
- [ ] Logic adheres to Spark 3.5.4 and Airflow 3.1.7 standards.
- [ ] Static resource allocation is prioritized over dynamic allocation (Spark).
- [ ] TaskFlow API and Datasets are used where appropriate (Airflow).

## 2. Testing & Validation
- [ ] New unit tests are added to the `tests/` directory.
- [ ] Existing tests pass: `python -m unittest discover tests`.
- [ ] (If bug fix) The failure is empirically reproduced before the fix.

## 3. Configuration & Security
- [ ] No hardcoded secrets or API keys.
- [ ] New settings are added to `src/core/config.py` using `BaseSettings`.
- [ ] Environment variable toggles are provided for Cloud/Local LLM switching.

## 4. Documentation
- [ ] `README.md` is updated if new features or API endpoints are added.
- [ ] Complex architectural decisions are documented in memory or comments.

## 5. SDLC Gate
- [ ] Changes are pushed to a feature branch.
- [ ] A Pull Request is opened.
- [ ] At least one successful review is received.
- [ ] CRITICAL issues flagged in review are resolved and re-reviewed.
