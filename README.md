# ABC Testing App

Бэкенд платформы для создания и прохождения тестов на **FastAPI** + **SQLAlchemy (async)**.

Учитель создаёт тесты с вопросами и вариантами ответов, ученик проходит их,
а система автоматически подсчитывает баллы.

## Архитектура

```
backend/app
├── api/v1        # HTTP-эндпоинты (роутеры)
├── core          # конфигурация, подключение к БД, безопасность
├── models        # SQLAlchemy-модели
├── schemas       # Pydantic-схемы (валидация запросов/ответов)
├── repositories  # доступ к данным (по одному репозиторию на модель)
├── services      # бизнес-логика
├── factory       # сборка сервисов с их зависимостями
└── main.py       # точка входа, подключение роутеров, создание таблиц
```

Слои: **API → Service → Repository → Model**. Сервисы собираются через `ServiceFactory`.

## Запуск

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env          # при необходимости отредактируйте DSN
uvicorn app.main:app --reload
```

Таблицы создаются автоматически при старте приложения (для локальной разработки).
Документация API доступна на `http://127.0.0.1:8000/docs`.

## Основные эндпоинты

| Метод  | Путь                                   | Назначение                          |
|--------|----------------------------------------|-------------------------------------|
| POST   | `/api/users/register`                  | Регистрация пользователя            |
| POST   | `/api/users/login`                     | Аутентификация                      |
| GET    | `/api/users/{user_id}`                 | Получить пользователя               |
| POST   | `/api/test/create?author_id=`          | Создать тест с вопросами            |
| GET    | `/api/test/`                           | Список опубликованных тестов        |
| GET    | `/api/test/{test_id}`                  | Тест целиком (для учителя)          |
| GET    | `/api/test/{test_id}/take`             | Тест для прохождения (без ответов)  |
| PATCH  | `/api/test/{test_id}`                  | Обновить тест                       |
| POST   | `/api/test/{test_id}/publish`          | Опубликовать тест                   |
| DELETE | `/api/test/{test_id}`                  | Удалить тест                        |
| POST   | `/api/attempt/start?user_id=`          | Начать попытку прохождения          |
| POST   | `/api/attempt/{attempt_id}/answer`     | Отправить ответ на вопрос           |
| POST   | `/api/attempt/{attempt_id}/finish`     | Завершить попытку и получить балл   |
| GET    | `/api/attempt/{attempt_id}`            | Получить попытку                    |
| POST   | `/api/group/`                          | Создать группу                      |
| POST   | `/api/group/{group_id}/students/{id}`  | Добавить ученика в группу           |
| GET    | `/api/group/{group_id}/students`       | Список учеников группы              |

## Подсчёт баллов

- **single_choice** — балл начисляется, если выбран единственный правильный вариант.
- **multiple_choice** — балл начисляется, если выбраны ровно все правильные варианты.

## Тесты

```bash
cd backend
pytest
```
