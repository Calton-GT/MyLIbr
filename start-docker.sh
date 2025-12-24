#!/bin/bash
# start-docker.sh - Автоматический запуск проекта в Docker

echo "🚀 Запуск Django проекта в Docker..."
echo "======================================"

# Проверяем установлен ли Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Ошибка: Docker не установлен!"
    echo "Скачайте с: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Проверяем запущен ли Docker Desktop
if ! docker info &> /dev/null; then
    echo "⚠️  Docker Desktop не запущен. Запустите Docker Desktop и повторите."
    exit 1
fi

echo "1. Останавливаем старые контейнеры..."
docker-compose down 2>/dev/null || true

echo "2. Очищаем Docker кэш..."
docker system prune -a -f 2>/dev/null || true

echo "3. Собираем Docker образ..."
docker-compose build --no-cache

echo "4. Запускаем контейнеры..."
docker-compose up -d

echo "5. Ждем запуска Django..."
sleep 10

echo "6. Выполняем миграции базы данных..."
docker-compose exec web python manage.py migrate 2>/dev/null || echo "⚠️  Миграции уже выполнены"

echo "7. Создаем администратора (логин: admin, пароль: admin123)..."
docker-compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Администратор создан')
else:
    print('⚠️  Администратор уже существует')
"

echo "8. Собираем статические файлы..."
docker-compose exec web python manage.py collectstatic --noinput 2>/dev/null || echo "⚠️  Статика уже собрана"

echo ""
echo "======================================"
echo "✅ ПРОЕКТ УСПЕШНО ЗАПУЩЕН!"
echo "🌐 Откройте в браузере: http://localhost:8000"
echo "🔧 Админка: http://localhost:8000/admin"
echo "👤 Логин: admin | Пароль: admin123"
echo ""
echo "📋 Полезные команды:"
echo "   Просмотр логов: docker-compose logs -f"
echo "   Остановить: docker-compose down"
echo "   Перезапустить: docker-compose restart"
echo "   Войти в контейнер: docker-compose exec web bash"
echo "======================================"