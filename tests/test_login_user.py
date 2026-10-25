import pytest
import allure
import api_methods


@allure.feature("Авторизация пользователя")
@allure.tag("auth", "login")
class TestUserLogin:

    @allure.title("Авторизация валидного пользователя")
    def test_login_valid_user(self, create_delete_user):
        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возврвщающую dict user_context"
        ):
            user_context = create_delete_user
            payload = {
                "email": user_context["email"],
                "password": user_context["password"],
            }
        with allure.step("Авторизуемся зарегистрированным ранее пользователем"):
            response = api_methods.post_login_user(payload)
        with allure.step("Проверяем, что статус код 200"):
            assert response.status_code == 200
        with allure.step(
            "Проверяем успешность авторизации зарегестрированного пользователя"
        ):
            data = response.json()
            assert data["success"]
            assert "accessToken" in data
            assert "refreshToken" in data

    @pytest.mark.parametrize(
        "allure_title, field_to_break, bad_value",
        [
            # Сценарий 1: Неверный email, пароль верный
            (
                "Проверка авторизации: неверный email, верный пароль",
                "email",
                "wrong_email_123@test.com",
            ),
            # Сценарий 2: Верный email, неверный пароль
            (
                "Проверка авторизации: верный email, неверный пароль",
                "password",
                "wrong_password_123",
            ),
            # Сценарий 3: Пустой email
            ("Проверка авторизации: пустой email", "email", ""),
            # Сценарий 4: Пустой пароль
            ("Проверка авторизации: пустой пароль", "password", ""),
        ],
    )
    def test_login_user_incorrect_data(
        self, allure_title, field_to_break, bad_value, create_delete_user
    ):
        allure.dynamic.title(allure_title)

        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возврвщающую dict user_context"
        ):
            user_context = create_delete_user
            valid_email = user_context["email"]
            valid_password = user_context["password"]

        with allure.step("Формируем payload с ошибкой"):
            payload = {"email": valid_email, "password": valid_password}
            # Подменяем нужное поле на ошибочное значение
            payload[field_to_break] = bad_value
        with allure.step("Отправляем запрос на авторизацию с некорректными данными"):
            response = api_methods.post_login_user(payload)

        with allure.step("Проверяем, что сервер отверг запрос"):
            # Обычно для ошибок авторизации возвращают 401 Unauthorized или 400 Bad Request.
            # Проверь документацию, какой статус ждет твой проект. Сейчас ставим 401 как самый частый вариант.
            assert (
                response.status_code == 401
            ), f"Ожидался код 401, но получен {response.status_code}"

        with allure.step("Проверяем структуру ответа об ошибке"):
            data = response.json()  # Десериализуем ответ

            # Флаг успеха должен быть False
            assert (
                data.get("success") is False
            ), "Флаг success должен быть False при ошибке"

            # В ответе должно быть сообщение об ошибке
            assert (
                data["message"] == "email or password are incorrect"
            ), "В ответе должно быть поле 'message' с описанием ошибки"
