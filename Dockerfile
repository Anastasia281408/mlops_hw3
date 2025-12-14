FROM python:3.11-slim
WORKDIR /app

# Копирование зависимостей и установка
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода и модели
COPY app/main.py .
COPY app/model.pkl .

# Версия по умолчанию, будет переопределена в compose-файлах
ENV MODEL_VERSION=v1.0.0 

# Запуск Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
