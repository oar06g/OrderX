# default service name
DOCKER_COMPOSE=docker-compose

# Define mysql variable
MYSQL_ROOT_PASSWORD=pass123
MYSQL_USER=orderx
MYSQL_PASSWORD=123123
AUTH_DB=auth_data
PRODUCTS_DB=productsdb
MYSQL_CONTAINER=mysqldb

.PHONY: all
all: build up init-db

.PHONY: build
build:
	$(DOCKER_COMPOSE) build

.PHONY: up
up:
	$(DOCKER_COMPOSE) up -d

.PHONY: init-db
init-db:
	@echo "Waiting for MySQL to be ready..."
	@until $(DOCKER_COMPOSE) exec -T $(MYSQL_CONTAINER) mysql -uroot -p$(MYSQL_ROOT_PASSWORD) -e "SELECT 1;" >/dev/null 2>&1; do \
		echo "MySQL is not ready yet..."; \
		sleep 3; \
	done
	@echo "Creating databases and user..."
	$(DOCKER_COMPOSE) exec -T $(MYSQL_CONTAINER) mysql -uroot -p$(MYSQL_ROOT_PASSWORD) -e "\
	CREATE DATABASE IF NOT EXISTS $(AUTH_DB); \
	CREATE DATABASE IF NOT EXISTS $(PRODUCTS_DB); \
	CREATE USER IF NOT EXISTS '$(MYSQL_USER)'@'%' IDENTIFIED BY '$(MYSQL_PASSWORD)'; \
	GRANT ALL PRIVILEGES ON $(AUTH_DB).* TO '$(MYSQL_USER)'@'%'; \
	GRANT ALL PRIVILEGES ON $(PRODUCTS_DB).* TO '$(MYSQL_USER)'@'%'; \
	FLUSH PRIVILEGES;"
	@echo "Databases and user created."
