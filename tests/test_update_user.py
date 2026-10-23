import pytest
import allure
import api_methods


@allure.feature("Изменение данных пользователя")
@allure.tag("auth", "user")
class TestUpdateUser:

    @allure.title(
        "Изменение данных о пользователе без авторизации пользователя"
    )  # нужна параметризация?
    def test_update_user_without_authorization(self, create_delete_user):
        with allure.step("Авторизуемся зарегистрированным ранее пользователем"):
            user_context = create_delete_user
        with allure.step("Отправляем patch без токена авторизации "):
            payload = {"email": "new_mail@mail.com"}
            response = api_methods.patch_update_user(None, **payload)
            data = response.json()
        with allure.step(
            "Проверяем ответ от сервера 401 False You Should be authorised"
        ):
            assert response.status_code == 401
            assert data["success"] == False
            assert data["message"] == "You should be authorised"

    @pytest.mark.parametrize(
        "allure_title, field_to_update, new_value",
        [
            (
                "Проверка обновления информации: email",
                "email",
                "new_email_123@test.com",
            ),
            (
                "Проверка обновления информации: password",
                "password",
                "new_password_123",
            ),
            (
                "Проверка обновления информации: user",
                "name",
                "new_user_123123123",
            ),
        ],
    )
    def test_update_user_with_authorization_success(
        self, create_delete_user, allure_title, field_to_update, new_value
    ):
        allure.dynamic.title(allure_title)
        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возврвщающую dict user_context"
        ):
            user_context = create_delete_user
        with allure.step(f"Меняем поле {field_to_update} с токеном авторизации "):
            payload = {field_to_update: new_value}
            response = api_methods.patch_update_user(
                user_context["access_token"], **payload
            )
        with allure.step("Проверяем, ответ 200 True и наличие user в ответе"):
            data = response.json()
            assert response.status_code == 200
            assert data["success"] == True
            assert "user" in data, " В ответе должно быть поле 'user'"

        with allure.step("Проверяем, что данные обновились,кроме теста с паролем"):
            if field_to_update == "password":
                print(
                    f"✅ Пароль успешно обновлен (статус 200). Значение не проверяется из соображений безопасности."
                )
            else:
                # Для email и name проверяем, что значение  изменилось
                assert (
                    data["user"][field_to_update] == new_value
                ), f"Поле {field_to_update} не обновилось. Ожидалось {new_value}, получено {data['user'].get(field_to_update)}"
