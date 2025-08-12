# Development commands

# Run the blog with hot reload
dev:
    uv run fastapi dev main.py --reload

# Format code
fmt:
    ruff format main.py
