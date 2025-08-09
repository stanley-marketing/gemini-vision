# Gemini Vision MCP Server Makefile

.PHONY: help install install-dev test lint format type-check clean run dev

# Default target
help:
	@echo "Available targets:"
	@echo "  install      - Install the package and dependencies"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code with black and isort"
	@echo "  type-check   - Run type checking with mypy"
	@echo "  clean        - Clean build artifacts"
	@echo "  run          - Run the MCP server"
	@echo "  dev          - Run in development mode"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Testing and quality
test:
	pytest tests/ -v

lint:
	flake8 src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

# Development
run:
	python -m gemini_vision.server

dev:
	python src/gemini_vision/server.py

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete

# Build
build:
	python setup.py sdist bdist_wheel

# Check everything before commit
check: format lint type-check test
	@echo "All checks passed!"