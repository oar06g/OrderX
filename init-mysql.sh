#!/bin/bash

COMPOSE_FILE="infra/docker-compose.yml"
MYSQL_CONTAINER="mysqldb"
MYSQL_ROOT_PASSWORD="pass123"

echo "⏳ Waiting for MySQL to be ready..."

# انتظر MySQL
until docker compose -f $COMPOSE_FILE exec -T $MYSQL_CONTAINER \
    mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "SELECT 1;" > /dev/null 2>&1; do
    echo "MySQL not ready yet..."
    sleep 5
done

echo "✔ MySQL is ready. Creating databases & users..."

docker compose -f $COMPOSE_FILE exec -T $MYSQL_CONTAINER mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "\
CREATE DATABASE IF NOT EXISTS auth_data; \
CREATE DATABASE IF NOT EXISTS productsdb; \
CREATE USER IF NOT EXISTS 'orderx'@'%' IDENTIFIED BY '123123'; \
GRANT ALL PRIVILEGES ON auth_data.* TO 'orderx'@'%'; \
GRANT ALL PRIVILEGES ON productsdb.* TO 'orderx'@'%'; \
FLUSH PRIVILEGES;"

echo "Databases & users created successfully!"
