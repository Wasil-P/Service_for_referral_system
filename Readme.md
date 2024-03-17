Стек
Приложение написано на django, библиотека djangorestframework.
База данных использовалась - SQLite
Для формирования ui документации использовался Swagger из библиотеки drf-yasg
Аутентификация реализована с помощью JWTAuthentication из библиотеки rest_framework_simplejwt

Навигация 
В пакете Service_for_referral_system находятся настройки для всего сервиса.
Базовые юрл и настройки в модулях urls.py и settings.py соответственно.
Файл swagger.py содержит настройти для UI документации.
Пакет Referral_system содержит пакет с самим API файл models.py с моделями, 
которые используються далее в пакете API.
В пакете API реализован весь функционал задания.