#!/bin/sh
# wait-for-db.sh - ждем когда база данных станет доступна

host="$1"
port="$2"
shift 2
cmd="$@"

until nc -z "$host" "$port"; do
  echo "⏳ Ждем базу данных $host:$port..."
  sleep 2
done

echo "✅ База данных доступна!"
exec $cmd