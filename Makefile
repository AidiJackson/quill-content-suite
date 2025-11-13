.PHONY: install run test lint format makemigration migrate clean help

help:
	@echo "Quillography Content Suite - Makefile commands:"
	@echo "  make install        - Install all dependencies"
	@echo "  make run            - Run the FastAPI server"
	@echo "  make test           - Run tests with pytest"
	@echo "  make lint           - Lint code with ruff"
	@echo "  make format         - Format code with black and isort"
	@echo "  make makemigration  - Create a new Alembic migration"
	@echo "  make migrate        - Run Alembic migrations"
	@echo "  make clean          - Clean up temporary files"

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v --tb=short

lint:
	ruff check app/ tests/

format:
	black app/ tests/
	isort app/ tests/
	ruff check --fix app/ tests/

makemigration:
	@read -p "Enter migration message: " message; \
	alembic revision --autogenerate -m "$$message"

migrate:
	alembic upgrade head

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f quillography.db
