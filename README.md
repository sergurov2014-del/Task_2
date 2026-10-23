## Задание 2: Api тесты

### Автотесты для проверки программы, которая помогает заказать бургер в Stellar Burgers

Данный проект представляет собой набор модулей для автоматического тестирования API веб сайта 
https://qa-stellarburgers.education-services.ru/api

### Реализованные сценарии

Созданы API тесты, покрывающие функционал:</br> 
`test_create_user` - Регистрации,
`test_update_user` - Обновления, 
`test_login_user` -  Авторизации пользователя, 
`test_create_order` - Создания,
`test_get_order` -  Получения пользователем заказа 

### Структура проекта

│   
├───allure_results - отчёт о тестировании
├───tests -пакет, содержащий тесты, разделенные по функциональности  (`test_create_order`, `test_create_user`, `test_get_order`, `test_login_user`,`test_update_user`) 
│   
│- `urls` - ссылки на тестируемые ресурсы
│- `conftest` -  фикстуры
│- `helpers` -  вспомогательные функции
│- `api_methods` - запросы к ручкам (API) 
│- `data_ingediens` - тестовые данные для создания заказов 
│- `.gitignore` - файлы коорые не будут загружены в git
│- `requremrnts` - нужные библиотеки сгенерированы автоматически -pigar generate
### Запуск автотестов

**Создание и установка зависимостей**
Создание requirements.txt
pip install pipreqs
pipreqs . --force --encoding=utf-8
Установка зависимостей
> `$ pip install -r requirements.txt`

**Запуск автотестов и создание Allure-report**

>  `$python -m  pytest ./tests --alluredir=allure_results`
>  `$allure serve allure_results`

Отладка производилась запуском автотестов
python -m pytest -v ./tests/