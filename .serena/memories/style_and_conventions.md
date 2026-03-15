# Style and Conventions

## Python Coding Standards
- **Versioning**: Python 3.8+ (currently using 3.10-slim in Docker).
- **Type Hinting**: All functions and methods MUST include type hints for parameters and return values.
- **Docstrings**: Use triple-quoted strings for class and function documentation.
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Variables: `snake_case`
  - Constants: `SCREAMING_SNAKE_CASE`

## Agentic Patterns (Agno)
- **Instructions**: Use `textwrap.dedent` for multi-line system prompts to maintain readability.
- **Tools**: Define async tools for external integrations (e.g., fetching SHS metrics).
- **Memory**: Use Agno's `MemoryManager` with a persistent database (`SqliteDb`) for stateful session context.

## Analytical Reports
- Every agentic response MUST follow the **Required Response Structure**:
  1. **[Technical Analysis]**: Root cause and bottleneck layer identification.
  2. **[Optimized Solution]**: Type-hinted Python code or configuration blocks.
  3. **[Architectural Notes]**: Warnings about resource consumption or maintenance.

## Testing Patterns
- Use the standard `unittest` framework.
- Each service (`SparkAnalyzerService`, `AirflowAnalyzerService`) must have a corresponding test file in `tests/`.
- Prioritize empirical reproduction of bottlenecks in tests.
