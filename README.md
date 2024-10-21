```bash
# Запуск проекта локально (БД в докере)
docker compose up -d # запуск только postgres
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Запуск проекта полностью в докере
docker compose --profile backend up -d # запуск postgres + python app
```

Если использовать `docker compose --profile backend up -d` - запустятся все сервисы, в которых указано `profiles: [backend]`