.DEFAULT_GOAL:=run

.PHONY: db-tmp
db-tmp:
	@poetry run scripts/setup-tmp-db.py

.PHONY: db-upgrade
db-upgrade:
	@FLASK_APP='utils:get_migration_app()' poetry run flask db upgrade

.PHONY: db-migrate
db-migrate: db-upgrade
	@echo "Please provide migration message"
	@read message; FLASK_APP='utils:get_migration_app()' poetry run flask db migrate -m "$$message"

.PHONY: run
run:
	@poetry run gunicorn --worker-class uvicorn.workers.UvicornWorker 'app:load_config_and_get_app()'

.PHONY: test
test:
	@tox
