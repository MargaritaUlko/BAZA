# Используем базовый образ с Python
FROM python:3.11-slim

# Установите необходимые системные зависимости
# Установите рабочий каталог
WORKDIR /fastapi_app

# Скопируйте файл requirements.txt
COPY requirements.txt .

# Установите зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте исходный код в контейнер
COPY . .

# Откройте порт 8000
EXPOSE 8000

# Определите команду для запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

#CMD ["gunicorn", "--version"]
# Установите системные зависимости, если нужны (не обязательно)
#RUN apt-get update && apt-get install -y \
#    gcc \
#    libffi-dev \
#    && rm -rf /var/lib/apt/lists/*

# Копируйте файл зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir gunicorn

# Установите зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Установите gunicorn
RUN pip install --no-cache-dir gunicorn

# Копируйте остальной код приложения
COPY . .

# Установите команду запуска приложения
CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
