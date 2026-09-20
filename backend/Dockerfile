FROM python:3.11-slim

WORKDIR /app

# Устанавливаем зависимости отдельным слоем для кэширования
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Код приложения
COPY app ./app

# Каталог для файла БД (SQLite), монтируется как volume
RUN mkdir -p /app/data
ENV DSN=sqlite+aiosqlite:///./data/app.db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
