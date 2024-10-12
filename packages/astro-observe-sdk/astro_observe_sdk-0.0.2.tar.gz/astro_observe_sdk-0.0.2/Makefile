.PHONY: check
check:
	@echo "Checking code..."
	@uv run mypy


.PHONY: test
test:
	@echo "Running tests..."
	@uv run -m pytest


.PHONY: build
build:
	@echo "Building..."
	@rm -rf dist/*
	@uv build
