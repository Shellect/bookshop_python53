.PHONY: help package_manager seed dev frontend build

# Переменные
IMAGE_NAME := poetry_manage

# Команды для выделения цветом текста в терминале
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "Available commands:"
	@echo " make package_manager ARGS=\"add <package name>\"     - Add python dependencies"
	@echo " make package_manager ARGS=\"add -D <package name>\"  - Add package as development dependencies"
	@echo " make package_manager ARGS=\"remove <package name>\"  - Remove python dependency"
	@echo " make seed NETWORK=\"bookshop_network\" ARGS=\"<path to seed script>\" - Seed database with test data"
	@echo " make dev      - Run development environment"
	@echo " make frontend - Build frontend bundle"
	@echo " make build    - Build production image"

# Poetry dependencies add/install/update/remove
package_manager:
	@echo "$(GREEN)Running poetry $(ARGS)$(NC)"
	docker build --target builder -t $(IMAGE_NAME):builder .
	docker run --rm -it \
		-v $(PWD)/pyproject.toml:/app/pyproject.toml \
		-v $(PWD)/poetry.lock:/app/poetry.lock \
		$(IMAGE_NAME):builder \
		poetry $(ARGS)

seed:
	@echo "$(GREEN)Seeding database$(NC)"
	FIXTURE=${FIXTURE} docker-compose --profile seed up

generate_migrations:
	COMMAND=${COMMAND} docker-compose --profile migrate up

dev:
	@echo "$(GREEN)Starting development environment$(NC)"
	docker compose up -d

frontend:
	@echo "$(GREEN)Building react bundle by Vite$(NC)"
	npm install
	npm run build

build:
	@echo "$(GREEN)Building production Docker image$(NC)"
	docker build --target production -t $(IMAGE_NAME):prouction .