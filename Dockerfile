# Используем базовый образ с Python
FROM python:3.11

# Установите рабочий каталог
WORKDIR /fastapi_app

# Скопируйте файл requirements.txt
COPY requirements.txt .

# Установите зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Установите uvicorn
RUN pip install uvicorn

# Проверьте установку uvicorn и выведите его путь
RUN which uvicorn

# Скопируйте исходный код в контейнер
COPY . .

# Откройте порт 8000
EXPOSE 8000

# Запустите приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
