import pytest
import helpers
import api_methods


@pytest.fixture
def create_delete_user():  # регистрация юзера и получение токенов
    # 1. ПОДГОТОВКА (До теста) создаём курьера возвращаем ответ user_context
    payload = helpers.new_user_data()
    response = api_methods.post_for_register_user(payload)
    data = response.json()
    raw_token = data.get("accessToken")
    if not raw_token:
        raise AssertionError(
            f"Не удалось найти accessToken в ответе сервера. Полный ответ: {data}"
        )
    # сохраняем блок который передастся в функцию
    user_context = {
        "email": payload["email"],
        "password": payload["password"],
        "access_token": raw_token,
        "payload": payload,
        "response": response,
    }
    yield user_context  # Передаем этот контейнер в тест

    access_token = user_context["access_token"]  # 2. ОЧИСТКА (После теста)

    delete_response = api_methods.del_delete_user(access_token)  # Вызываем удаление
