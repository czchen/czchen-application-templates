.DEFAULT_GOAL:=run

.PHONY: db-tmp
db-tmp:
	poetry run scripts/setup-tmp-db.py

.PHONY: db-upgrade
db-upgrade:
	FLASK_APP='utils:get_migration_app()' poetry run flask db upgrade

.PHONY: db-migrate
db-migrate:
	@echo "Please provide migration message"
	@read message; FLASK_APP='utils:get_migration_app()' poetry run flask db migrate -m "$$message"

.PHONY: run
run:
	FLASK_APP='app:load_config_and_get_flask_app()' poetry run flask run
