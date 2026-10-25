import allure
import api_methods
import data_ingediens as D
from random import sample


@allure.feature("Получение заказов конкретного пользователя")
@allure.tag("orders")
class TestGetOrder:

    @allure.title("Получение заказов без авторизации пользователя ")
    def test_get_order_without_authorization(self):
        with allure.step("Отправляем post на получение заказа без токена авторизации "):
            response = api_methods.get_user_orders(None)

        with allure.step("Проверяем ответ от сервера 401 False"):
            data = response.json()
            assert response.status_code == 401
            assert data["success"] == False
            assert data["message"] == "You should be authorised"

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_order_with_authorization(self, create_delete_user):
        with allure.step(
            "Вызываем фикстуру,создающую/удаляющую user и возврвщающую dict user_context"
        ):
            user_context = create_delete_user
            access_token = user_context["access_token"]
        with allure.step("Подготавливаем список из 3 рандомных ингридиентов"):
            ingredients = sample(D.LIST_ID, 3)
        with allure.step("Отправляем post на создание заказа с токеном авторизации"):
            response = api_methods.post_create_order(access_token, ingredients)
        with allure.step("Отправляем post на получение заказа с токеном авторизации "):
            response = api_methods.get_user_orders(access_token)
        with allure.step("Проверяем ответ от сервера 200 True"):
            data = response.json()
            assert response.status_code == 200
            assert data["success"] == True
        with allure.step("Проверяем наличие total и totalToday в ответе"):
            assert data["total"]
            assert data["totalToday"]
        with allure.step(
            "Проверяем наличие _id, ingredients, status, name, number в первом из заказов ответа"
        ):
            assert data["orders"][0]["_id"]
            assert data["orders"][0]["ingredients"]
            assert data["orders"][0]["status"]
            assert data["orders"][0]["name"]
            assert data["orders"][0]["number"]
