import uuid  # библиотека для создания уникальных идентификаторов


def random_id():
    u_id = str(uuid.uuid4())[:5]
    return u_id


def new_user_data():  # генерируем данные рандомного юзера
    user_id = random_id()
    user_data = {
        "email": f"test_user_{user_id}@ya.ru",
        "password": "testpassword123",
        "name": f"Test_ User_{user_id}",
    }

    return user_data