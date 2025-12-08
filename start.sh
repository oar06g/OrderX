#!/bin/bash

COMPOSE_FILE="infra/docker-compose.yml"
MYSQL_SERVICE="mysql"

echo "🚀 Starting smart startup process..."

##############################################
# Step 1 — Start MySQL only
##############################################
echo "⏳ Starting MySQL service..."
docker compose -f $COMPOSE_FILE up -d $MYSQL_SERVICE

if [ $? -ne 0 ]; then
    echo "❌ Failed to start MySQL!"
    exit 1
fi

##############################################
# Step 2 — Wait until MySQL becomes ready
##############################################
echo "⏳ Waiting for MySQL to become healthy..."

# smart wait — checks container logs for “ready”
until docker compose -f $COMPOSE_FILE exec -T $MYSQL_SERVICE \
    mysql -uroot -ppass123 -e "SELECT 1;" > /dev/null 2>&1; do
    
    echo "   ↳ MySQL still not ready..."
    sleep 3
done

echo "✔ MySQL is ready!"

##############################################
# Step 3 — Run MySQL initialization script
##############################################
echo "⚙ Running init-mysql.sh ..."
chmod +x ./init-mysql.sh
./init-mysql.sh

if [ $? -ne 0 ]; then
    echo "❌ init-mysql.sh failed!"
    exit 1
fi

echo "✔ init-mysql.sh completed successfully!"

##############################################
# Step 4 — Start the remaining services
##############################################
echo "🚀 Starting all remaining services..."

docker compose -f $COMPOSE_FILE up -d kafka auth products nginx

if [ $? -ne 0 ]; then
    echo "❌ Failed to start one or more services!"
    exit 1
fi

echo "🎉 All services started successfully!"
