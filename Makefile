## ----------------------------------------------------------------------
## Makefile for Timeseries Data Visualization challenge.
##
## Used in both development and production. See targets below.
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

terminal:  ## Open terminal in running docker development container
	docker-compose exec web /bin/bash

shell:  ## Open django shell in running docker development container
	docker-compose exec web python manage.py shell
	
migrations: # make development migrations
	docker-compose exec web python manage.py makemigrations

migrate: # development migrate 
	docker-compose exec web python manage.py migrate

dev_superuser: # make development superuser 
	docker-compose exec web python manage.py createsuperuser


# ---------- Checks and tests ---------- #
test: ## Execute tests within the docker image
	docker-compose exec web python manage.py test



# ---------- Production ---------- #
production_stop: ## Stop production server
	docker-compose -f docker-compose.prod.yml down --remove-orphans

production_start: ## Start production server as daemon
	docker-compose -f docker-compose.prod.yml up --build --remove-orphans -d

production_djangologs: ## Show django logs
	docker logs sensordatakristianmscom_web_1

production_accesslogs: ## Show nginx access logs
	docker logs sensordatakristianmscom_nginx_1

production_terminal: # Open shell in running docker production container
	docker-compose -f docker-compose.prod.yml exec web /bin/bash

production_shell:  ## Open django shell in running docker development container
	docker-compose -f docker-compose.prod.yml exec web python manage.py shell

