## ----------------------------------------------------------------------
## Makefile for Timeseries Data Visualizatio challenge.
##
## Used in development.
## ----------------------------------------------------------------------

help:   # Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)
	

# ---------- Development ---------- #
build:  ## Build or rebuild development docker image
	docker-compose build

develop:  ## Run development server
	docker-compose up --remove-orphans


stop: ## Stop development server
	docker-compose down --remove-orphans

shell:  ## Open shell in running docker development container
	docker-compose exec web /bin/bash

migrations: # make development migrations
	docker-compose exec web python manage.py makemigrations

migrate: # development migrate 
	docker-compose exec web python manage.py migrate

dev_superuser: # make development superuser 
	docker-compose exec web python manage.py createsuperuser


# ---------- Checks and tests ---------- #
test: ## Execute tests within the docker image
	docker-compose exec web python manage.py test


