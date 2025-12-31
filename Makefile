.PHONY: help install serve lint test clean

# Default target
help:
	@echo "Chowdeck Restaurant API - Make Commands"
	@echo "========================================"
	@echo "make install    - Install dependencies in virtual environment"
	@echo "make serve      - Run development server"
	@echo "make lint       - Run linter and formatter checks"
	@echo "make format     - Auto-format code with Black"
	@echo "make test       - Run test suite with coverage"
	@echo "make clean      - Remove cache and build files"

# Install dependencies
install:
	@echo "Installing dependencies..."
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

# Run development server
serve:
	@echo "Starting Flask development server..."
	python3 -m src.main

# Lint code
lint:
	@echo "Running flake8..."
	flake8 src/ tests/ --max-line-length=100 --exclude=__pycache__,*.pyc
	@echo "Running mypy..."
	mypy src/ --ignore-missing-imports

# Format code
format:
	@echo "Formatting code with Black..."
	black src/ tests/ --line-length=100

# Run tests
test:
	@echo "Running tests with coverage..."
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Clean cache files
clean:
	@echo "Cleaning cache and build files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache
	@echo "Clean complete!"
