#!/bin/bash
# stop-docker.sh - Остановка Docker контейнеров

echo "🛑 Остановка Docker контейнеров..."
docker-compose down
docker system prune -f
echo "✅ Контейнеры остановлены и очищены!"