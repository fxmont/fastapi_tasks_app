### Установить just (опционально)

just (justfile) позволяет быстро запускать команды ([подробнее тут](https://github.com/casey/just?tab=readme-ov-file#packages))

Debian/Ubuntu:
```shell
apt install just
```

---

## Команды для управления проектом

### Запустить Docker с FastAPI и PostgreSQL
Используя just:
```shell
just up
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml up --build
```

### Остановить Docker контейнеры
Используя just:
```shell
just stop
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml down
```

### Удалить Docker контейнеры и данные
Используя just:
```shell
just erase
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml down -v
```

### Просмотреть логи приложения
Используя just:
```shell
just logs
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "cat /app/app.log"
```

### Просмотреть логи приложения в реальном времени
Используя just:
```shell
just logstail
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi sh -c "tail -f /app/app.log"
```

### Создать новую миграцию через Alembic
Используя just:
```shell
just mm "описание миграции"
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic revision --autogenerate -m "описание миграции"
```

### Применить миграции через Alembic
Используя just:
```shell
just migrate
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic upgrade head
```

### Откатить миграцию через Alembic
Используя just:
```shell
just downgrade версия
```

Или командой:
```shell
docker compose -f docker-compose.dev.yml exec fastapi poetry run alembic downgrade версия
```
