set shell := ["bash", "-cu"]
set windows-shell := ["powershell"]

pkg := "package"

# Default action
_:
    just lint
    just fmt
    just test

# Install
i:
    uv sync --all-packages

# Set up the project
setup:
    brew install ls-lint typos-cli
    just i

# Lint the code
lint:
    ls-lint
    typos
    uv run ruff check --fix

# Format the code
fmt:
    uv run ruff format

# Run tests
test:
    uv run pytest

# Build the package
build:
    uv build --package jder_fastapi --out-dir ./{{pkg}}/dist

# Run example
example:
    cd example && uv run fastapi dev main.py --port 4001

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
