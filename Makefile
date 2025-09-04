
project_dir := .
package_dir := app

##@ Formatting & Linting

.PHONY: reformat
reformat: ## Reformat code
	@uv run ruff format $(project_dir)
	@uv run ruff check $(project_dir) --fix

.PHONY: lint
lint: reformat ## Lint code
	@uv run mypy $(project_dir)

##@ App commands

.PHONY: run
run: ## Run bot
	@uv run python -O -m $(package_dir)

.PHONY: app-build
app-build: ## Build bot image
	@docker compose build

.PHONY: app-run
app-run: ## Run bot in docker container
	@docker compose stop
	@docker compose up -d --remove-orphans

.PHONY: app-stop
app-stop: ## Stop docker containers
	@docker compose stop

.PHONY: app-down
app-down: ## Down docker containers
	@docker compose down

.PHONY: app-destroy
app-destroy: ## Destroy docker containers
	@docker compose down -v --remove-orphans

.PHONY: app-logs
app-logs: ## Show bot logs
	@docker compose logs -f bot

##@ Other

.PHONY: name
name: ## Get top-level package name
	@echo $(package_dir)
