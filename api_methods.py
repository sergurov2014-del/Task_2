import requests
import urls


def post_for_register_user(payload: dict) -> requests.Response:
    # отправляет POST-запрос для регистрации пользователя
    response = requests.post(
        urls.URL_REGISTER,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return response


def post_login_user(payload) -> requests.Response:
    # отправляет POST-запрос для авторизациии пользователя

    response = requests.post(
        urls.URL_LOGIN,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return response


def post_logout(refreshToken: str) -> requests.Response:
    #  отправляет POST-запрос для выхода юзера из профиля
    payload = {"token": f"{refreshToken}"}
    response = requests.post(
        urls.URL_LOGOUT,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    return response


def patch_update_user(access_token: str, **kwargs) -> requests.Response:
    # отправляет PATCH-запрос на изменение данных пользователя
    # access_token - токен авторизации
    # **kwargs  - поля для обновления (email, password, name)
    response = requests.patch(
        urls.URL_USER,
        json=kwargs,
        headers={
            "Content-Type": "application/json",
            "Authorization": access_token,
        },
    )
    return response


def del_delete_user(access_token: str) -> requests.Response:
    # удаляет пользователя по accessToken - удаление юзера после тестов
    #  access_token - токен авторизации
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token,
    }

    response = requests.delete(urls.URL_USER, headers=headers)

    return response


def get_ingredients() -> requests.Response:
    # отправляет GET-запрос на получение списка ингредиентов
    response = requests.get(urls.URL_INGEDIENTS)
    return response  # возвращает запрос со списком ингридиентов


def post_create_order(access_token: str, ingredients: list) -> requests.Response:
    # отправляет POST-запрос на создание заказа.
    # ingredients - список из ID ингредиентов, получить инг-ы get_ingredients()
    headers = {
        "Content-Type": "application/json",
        "Authorization": access_token,
    }

    response = requests.post(
        urls.URL_ORDERS, json={"ingredients": ingredients}, headers=headers
    )

    return response


def get_user_orders(access_token: str = "") -> requests.Response:
    # Отправляет GET-запрос на получение заказов пользователя
    # ? токен авторизации необязателен, если его не будет 401 Unauthorixed
    headers = {"Content-Type": "application/json", "Authorization": access_token}
    response = requests.get(urls.URL_ORDERS, headers=headers)
    return response
