# Development commands for audrey.feldroy.com

# Run the blog in development mode with reload
dev:
    uv run fastapi dev main.py --reload

# Format code with ruff
format:
    ruff format main.py

# Lint code with ruff
lint:
    ruff check main.py

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

# Show available commands
list:
    @just --list
