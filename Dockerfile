# Используем базовый образ с Python
FROM python:3.12

# Установите рабочий каталог
WORKDIR /fastapi_app

RUN pip install pycryptodome

# Скопируйте файл requirements.txt
COPY requirements.txt .

# Установите зависимости из requirements.txt
RUN pip install -r requirements.txt

# Установите uvicorn
RUN pip install uvicorn

# Проверьте установку uvicorn и выведите его путь
RUN which uvicorn

# Скопируйте исходный код в контейнер
COPY . .

# Откройте порт 8000
EXPOSE 2000

# Запустите приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2000"]
