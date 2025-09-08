import pytest
import requests
import random
import string

# 🔑 Наставник, запиши пожалуйста сюда свой КЛЮЧ
API_KEY = "Наставник, запиши пожалуйста сюда свой КЛЮЧ"

BASE_URL = "https://ru.yougile.com/api-v2"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_random_name():
    return "Test Project " + "".join(random.choices(string.ascii_letters, k=6))


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def headers():
    return HEADERS


@pytest.fixture
def client(headers, base_url):
    class Client:
        def create_project(self, title):
            """Создание проекта — возвращает только ID"""
            url = f"{base_url}/projects"
            data = {"title": title}
            response = requests.post(url, json=data, headers=headers)
            return response.json(), response.status_code

        def get_project(self, project_id):
            """Получение проекта по ID"""
            url = f"{base_url}/projects/{project_id}"
            response = requests.get(url, headers=headers)
            json_response = response.json()
            # Извлекаем из content, если есть
            if "content" in json_response:
                return json_response["content"], response.status_code
            return json_response, response.status_code

        def update_project(self, project_id, title=None, archived=None):
            """Обновление проекта"""
            url = f"{base_url}/projects/{project_id}"
            data = {}
            if title is not None:
                data["title"] = title
            if archived is not None:
                data["archived"] = archived
            response = requests.put(url, json=data, headers=headers)
            json_response = response.json()
            if "content" in json_response:
                return json_response["content"], response.status_code
            return json_response, response.status_code

    return Client()


# === Тесты ===

def test_create_project_positive(client):
    """Позитивный: создание проекта с валидным названием"""
    title = generate_random_name()
    data, status = client.create_project(title)

    assert status == 201, f"Ожидался статус 201, получен {status}"
    assert "id" in data, "В ответе нет ID проекта"
    project_id = data["id"]

    # Проверим, что проект действительно создан с нужным названием
    project_data, status_get = client.get_project(project_id)
    assert status_get == 200, f"Не удалось получить проект после создания"
    assert project_data["title"] == title, "Название проекта не совпадает"

    # Проверяем archived, только если поле присутствует
    if "archived" in project_data:
        assert project_data["archived"] is False, "Проект должен быть не в архиве"
    else:
        print("⚠️ Поле 'archived' отсутствует в ответе — пропускаем проверку")

    print(f"✅ Проект создан и проверен: {project_data['title']} (ID: {project_id})")


def test_create_project_negative_no_title(client):
    """Негативный: попытка создать проект без названия"""
    data, status = client.create_project(title="")

    assert status == 400, f"Ожидался статус 400, получен {status}"
    assert "error" in data or "message" in data
    assert "title should not be empty" in str(data.get("message", ""))
    print("✅ Корректно отклонён проект без названия")


def test_get_project_positive(client):
    """Позитивный: получение существующего проекта"""
    title = generate_random_name()
    new_project, _ = client.create_project(title)
    project_id = new_project["id"]

    data, status = client.get_project(project_id)

    assert status == 200, f"Ожидался статус 200, получен {status}"
    assert data["id"] == project_id
    assert data["title"] == title
    print(f"✅ Проект получен: {data['title']}")


def test_get_project_negative_not_found(client):
    """Негативный: попытка получить несуществующий проект"""
    invalid_id = "00000000-0000-0000-0000-000000000000"
    data, status = client.get_project(invalid_id)

    assert status == 404, f"Ожидался статус 404, получен {status}"
    assert "error" in data
    print("✅ Корректно обработан запрос к несуществующему проекту")


def test_update_project_positive(client):
    """Позитивный: обновление названия проекта"""
    old_title = generate_random_name()
    new_title = old_title + " (updated)"
    project_data, _ = client.create_project(old_title)
    project_id = project_data["id"]

    updated_data, status = client.update_project(project_id, title=new_title)

    assert status == 200, f"Ожидался статус 200, получен {status}"

    # Проверим через GET, что название обновилось
    refreshed_data, _ = client.get_project(project_id)
    assert refreshed_data["title"] == new_title
    print(f"✅ Проект обновлён: {refreshed_data['title']}")


def test_update_project_negative_invalid_id(client):
    """Негативный: попытка обновить проект с неверным форматом ID"""
    invalid_id = "invalid-uuid-format"
    data, status = client.update_project(invalid_id, title="New Title")

    assert status in (400, 404), f"Ожидался статус 400 или 404, получен {status}"
    assert "error" in data
    print("✅ Корректно отклонён запрос с неверным ID")