# Development commands for audrey.feldroy.com

# Show available commands
list:
    @just --list

# Run the blog in development mode with reload
run: 
    @lsof -ti tcp:8000 | xargs kill -9 || true
    uv run fastapi dev main.py --reload

# Format and fix code with ruff
fix:
    ruff format main.py
    ruff check main.py --fix

# Run tests
test:
    uv run pytest

# Sync dependencies
sync:
    uv sync

# Install development dependencies
install:
    uv sync --group dev

# Clean cache files
clean:
    rm -rf __pycache__ .pytest_cache .ruff_cache
