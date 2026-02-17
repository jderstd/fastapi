set shell := ["bash", "-cu"]
set windows-shell := ["pwsh", "-Command"]

pkg := "package"

# Default action
_:
    just fmt
    just lint
    just type
    just test

# Install
i:
    uv sync --all-packages

# Format the code
fmt:
    uv run ruff format

# Lint the code
lint:
    ls-lint -config ./.ls-lint.yaml
    typos
    uv run ruff check --fix

# Check types
type:
    uv run ty check

# Run tests
test:
    uv run pytest

# Build the package
build:
    uv build --package jder_fastapi --out-dir ./{{pkg}}/dist

# Run example
example:
    cd example && uv run fastapi dev main.py --port 4001

# Publish package as dry-run
publish-try:
    cd ./{{pkg}} && uv publish --dry-run

# Publish package
publish:
    cd ./{{pkg}} && uv publish

# Clean caches
clean:
    cd ./{{pkg}} && rm -rf ./dist
    rm -rf .pytest_cache
    rm -rf .ruff_cache
    find . -type d -name "__pycache__" -exec rm -rf {} +

# Clean everything
clean-all:
    just clean
    rm -rf .venv
