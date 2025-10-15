# Makefile for NLQ Full-Stack App

.PHONY: help setup dev test lint clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup the entire project
	@echo "🚀 Setting up NLQ Full-Stack Application..."
	@chmod +x setup.sh
	@./setup.sh

dev-backend: ## Start backend development server
	@cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start frontend development server
	@cd frontend && npm run dev

dev: ## Start both backend and frontend in development mode
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop all servers"
	@trap 'kill 0' EXIT; \
	cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
	cd frontend && npm run dev & \
	wait

test-backend: ## Run backend tests
	@cd backend && source venv/bin/activate && pytest

test-frontend: ## Run frontend tests
	@cd frontend && npm test

test: ## Run all tests
	@echo "Running backend tests..."
	@cd backend && source venv/bin/activate && pytest
	@echo "Running frontend tests..."
	@cd frontend && npm test

lint-backend: ## Lint backend code
	@cd backend && source venv/bin/activate && ruff check . && black . && mypy .

lint-frontend: ## Lint frontend code
	@cd frontend && npm run lint && npm run type-check

lint: ## Lint all code
	@echo "Linting backend..."
	@cd backend && source venv/bin/activate && ruff check . && black . && mypy .
	@echo "Linting frontend..."
	@cd frontend && npm run lint && npm run type-check

docker-up: ## Start Docker services
	@docker-compose up -d

docker-down: ## Stop Docker services
	@docker-compose down

docker-logs: ## Show Docker logs
	@docker-compose logs -f

db-migrate: ## Run database migrations
	@docker-compose exec backend alembic upgrade head

db-seed: ## Seed database with sample data
	@docker-compose exec backend python -c "from app.core.seed_data import generate_sample_data; generate_sample_data()"

clean: ## Clean up generated files
	@echo "Cleaning up..."
	@rm -rf backend/venv
	@rm -rf frontend/node_modules
	@rm -rf frontend/.next
	@rm -f .env
	@echo "Cleanup complete!"
