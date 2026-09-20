import uuid

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


def _login():
    return f"user_{uuid.uuid4().hex[:10]}"


async def _register(client: AsyncClient, role: str = "student") -> dict:
    payload = {"login": _login(), "password": "password123", "role": role}
    resp = await client.post("/api/users/register", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


async def test_health(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


async def test_register_and_login(client: AsyncClient):
    login = _login()
    payload = {"login": login, "password": "password123", "role": "teacher"}

    resp = await client.post("/api/users/register", json=payload)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["login"] == login
    assert body["role"] == "teacher"
    assert "password" not in body  # пароль не должен возвращаться

    # повторная регистрация — конфликт
    resp = await client.post("/api/users/register", json=payload)
    assert resp.status_code == 409

    # успешный логин
    resp = await client.post("/api/users/login", json={"login": login, "password": "password123"})
    assert resp.status_code == 200

    # неверный пароль
    resp = await client.post("/api/users/login", json={"login": login, "password": "wrongpass1"})
    assert resp.status_code == 401


async def test_full_testing_flow(client: AsyncClient):
    teacher = await _register(client, role="teacher")
    student = await _register(client, role="student")

    # учитель создаёт тест с одним вопросом single_choice
    test_body = {
        "test_data": {"title": "Математика", "description": "Простой тест"},
        "questions": [
            {
                "text": "2 + 2 = ?",
                "question_type": "single_choice",
                "order_index": 1,
                "points": 2.0,
                "options": [
                    {"text": "3", "is_correct": False, "order_index": 1},
                    {"text": "4", "is_correct": True, "order_index": 2},
                ],
            }
        ],
    }
    resp = await client.post(f"/api/test/create?author_id={teacher['Id']}", json=test_body)
    assert resp.status_code == 201, resp.text
    test = resp.json()
    test_id = test["Id"]
    question = test["questions"][0]
    correct_option = next(o for o in question["options"] if o["is_correct"])

    # публикуем тест
    resp = await client.post(f"/api/test/{test_id}/publish")
    assert resp.status_code == 200
    assert resp.json()["is_published"] is True

    # тест виден в списке опубликованных
    resp = await client.get("/api/test/")
    assert resp.status_code == 200
    assert any(t["Id"] == test_id for t in resp.json())

    # версия для прохождения не раскрывает правильные ответы
    resp = await client.get(f"/api/test/{test_id}/take")
    assert resp.status_code == 200
    take = resp.json()
    assert "is_correct" not in take["questions"][0]["options"][0]

    # ученик начинает попытку
    resp = await client.post(f"/api/attempt/start?user_id={student['Id']}", json={"test_id": test_id})
    assert resp.status_code == 201, resp.text
    attempt_id = resp.json()["Id"]

    # отправляет правильный ответ
    resp = await client.post(
        f"/api/attempt/{attempt_id}/answer",
        json={
            "attempt_id": attempt_id,
            "question_id": question["Id"],
            "selected_option_id": correct_option["Id"],
        },
    )
    assert resp.status_code == 201, resp.text

    # завершает попытку — балл равен points вопроса
    resp = await client.post(f"/api/attempt/{attempt_id}/finish")
    assert resp.status_code == 200, resp.text
    finished = resp.json()
    assert finished["score"] == 2.0
    assert finished["finished_at"] is not None

    # повторное завершение запрещено
    resp = await client.post(f"/api/attempt/{attempt_id}/finish")
    assert resp.status_code == 400


async def test_wrong_answer_scores_zero(client: AsyncClient):
    teacher = await _register(client, role="teacher")
    student = await _register(client, role="student")

    test_body = {
        "test_data": {"title": "История", "description": None},
        "questions": [
            {
                "text": "Столица Франции?",
                "question_type": "single_choice",
                "order_index": 1,
                "points": 5.0,
                "options": [
                    {"text": "Париж", "is_correct": True, "order_index": 1},
                    {"text": "Берлин", "is_correct": False, "order_index": 2},
                ],
            }
        ],
    }
    resp = await client.post(f"/api/test/create?author_id={teacher['Id']}", json=test_body)
    assert resp.status_code == 201, resp.text
    test = resp.json()
    question = test["questions"][0]
    wrong_option = next(o for o in question["options"] if not o["is_correct"])

    resp = await client.post(f"/api/attempt/start?user_id={student['Id']}", json={"test_id": test["Id"]})
    attempt_id = resp.json()["Id"]

    await client.post(
        f"/api/attempt/{attempt_id}/answer",
        json={
            "attempt_id": attempt_id,
            "question_id": question["Id"],
            "selected_option_id": wrong_option["Id"],
        },
    )
    resp = await client.post(f"/api/attempt/{attempt_id}/finish")
    assert resp.status_code == 200
    assert resp.json()["score"] == 0.0


async def test_update_and_delete_test(client: AsyncClient):
    teacher = await _register(client, role="teacher")
    test_body = {
        "test_data": {"title": "Черновик", "description": "старое"},
        "questions": [],
    }
    resp = await client.post(f"/api/test/create?author_id={teacher['Id']}", json=test_body)
    test_id = resp.json()["Id"]

    resp = await client.patch(f"/api/test/{test_id}", json={"title": "Обновлённый"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Обновлённый"

    resp = await client.delete(f"/api/test/{test_id}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/test/{test_id}")
    assert resp.status_code == 404


async def test_group_management(client: AsyncClient):
    student = await _register(client, role="student")

    resp = await client.post("/api/group/", json={"name": "10-А"})
    assert resp.status_code == 201, resp.text
    group_id = resp.json()["Id"]

    resp = await client.post(f"/api/group/{group_id}/students/{student['Id']}")
    assert resp.status_code == 200
    assert resp.json()["group_id"] == group_id

    resp = await client.get(f"/api/group/{group_id}/students")
    assert resp.status_code == 200
    students = resp.json()
    assert any(s["Id"] == student["Id"] for s in students)
