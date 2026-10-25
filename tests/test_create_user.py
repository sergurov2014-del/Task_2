import pytest
import allure
import api_methods
import helpers


@allure.feature("Регистрация пользователя")
@allure.tag("auth", "register")
class TestUserRegistration:

    @allure.title("Регистрация уникального пользователя")
    def test_unique_user_registration(self, create_delete_user):
        with allure.step(
            "Создаём пользователя, через фикстуру- в конце она удалит пользователя "
        ):
            user_context = create_delete_user
        with allure.step("Получаем данные для проверки"):
            data = user_context["response"].json()

        with allure.step("Проверяем наличие токенов в данных от фикстуры"):
            assert data["accessToken"]
            assert data["refreshToken"]
            assert data["user"]["email"].startswith("test_")

    @allure.title("Повторная регистрация пользователя возвращает 403 forbidden")
    def test_create_two_equal_users_return_403_forbidden(self, create_delete_user):
        with allure.step(
            "Создаём пользователя, через фикстуру- в конце она удалит пользователя "
        ):
            user_context = create_delete_user
        with allure.step("Формируем payload с email, password, name пользователя"):
            payloads = user_context["payload"]
        with allure.step(
            "Отправляем повторный запрос на создание уже созданного пользователя"
        ):
            response = api_methods.post_for_register_user(payloads)
        with allure.step("Проверяем возвращение 403 forbidden"):
            data_error = response.json()
            assert response.status_code == 403
            assert data_error["success"] == False
            assert data_error["message"] == "User already exists"

    @pytest.mark.parametrize(
        "allure_title, without_field",
        [
            (
                "Проверка регистрации пользователя без email",
                "email",
            ),
            (
                "Проверка регистрации курьера без пароля",
                "password",
            ),
            (
                "Проверка регистрации курьера без имени",
                "name",
            ),
        ],
    )
    def test_create_courier_missing_required_field_returns_400(
        self, allure_title, without_field
    ):
        # меняем заголовок allure после каждой итерации
        allure.dynamic.title(allure_title)
        with allure.step(f"Формируем payload с пустым полем {without_field}"):
            payload_user_without_field = helpers.new_user_data()
            payload_user_without_field[without_field] = ""
        with allure.step(
            f"Отправляем запрос на создание пользователя без обязательного поля {without_field}"
        ):
            response = api_methods.post_for_register_user(payload_user_without_field)
            data = response.json()
        with allure.step("Проверяем возвращение 403 forbidden"):

            assert response.status_code == 403
            assert data["success"] == False
            assert data["message"] == "Email, password and name are required fields"
