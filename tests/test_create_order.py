import allure
import api_methods
import data_ingediens as D
from random import sample


@allure.feature("Создание заказа")
@allure.tag("orders")
class TestCreateOrder:

    @allure.title("Создание заказа без авторизации пользователя (гостевой заказ)")
    def test_create_order_without_authorization(self):
        with allure.step("Подготавливаем список из 2 рандомных ингридиентов"):
            ingredients = sample(D.LIST_ID, 2)
        with allure.step("Отправляем post на создание заказа без токена авторизации "):
            response = api_methods.post_create_order(None, ingredients)

        with allure.step(
            "Проверяем ответ от сервера 200 True, наличие названия и номера заказа"
        ):
            data = response.json()
            assert response.status_code == 200
            assert data["success"]
            assert data["order"]["number"]
            assert data["name"]

    @allure.title("Создание заказа с авторизацией пользователя с ингридиентами ")
    def test_create_order_with_authorization_success(self, create_delete_user):
        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возврвщающую dict user_context"
        ):
            user_context = create_delete_user
            access_token = user_context["access_token"]
        with allure.step("Подготавливаем список из 3 рандомных ингридиентов"):
            ingredients = sample(D.LIST_ID, 3)
        with allure.step("Отправляем post на создание заказа с токеном авторизации"):
            response = api_methods.post_create_order(access_token, ingredients)
        with allure.step(
            "Проверяем ответ от сервера 200 True, наличие названия и номера заказа"
        ):
            data = response.json()
            assert response.status_code == 200
            assert data["success"]
            assert data["order"]["number"]
            assert data["name"]

    @allure.title("Создание заказа с  авторизацией пользователя, но без ингридиентов")
    def test_create_order_no_ingedients_with_authorization_(self, create_delete_user):
        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возвращающую dict user_context"
        ):
            user_context = create_delete_user
            access_token = user_context["access_token"]
        with allure.step("Список ингридиентов пустой"):
            ingredients = []
        with allure.step("Отправляем post на создание заказа с токеном авторизации"):
            response = api_methods.post_create_order(access_token, ingredients)
        with allure.step("Проверяем ответ от сервера 400 False "):
            data = response.json()

            assert response.status_code == 400
            assert data["success"] == False
            assert data["message"] == "Ingredient ids must be provided"

    @allure.title(
        "Создание заказа с  авторизацией пользователя, с неверным хэшем ингридиентов"
    )
    def test_create_order_incorrect_ingedient_with_authorization(
        self, create_delete_user
    ):
        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возвращающую dict user_context"
        ):
            user_context = create_delete_user
            access_token = user_context["access_token"]
        with allure.step("Создаём список с 1 некорректным хэшем"):
            ingredients = ["invalid_hash_666!"]

        with allure.step("Отправляем post на создание заказа с токеном авторизации"):
            response = api_methods.post_create_order(access_token, ingredients)
        with allure.step("Проверяем ответ от сервера 500 False"):
            assert response.status_code == 500
