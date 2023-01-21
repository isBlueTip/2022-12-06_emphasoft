# 12_06_emphasoft

## Описание

API для бронирования гостиничных номеров с авторизацией по токену с развёртыванием в docker-compose

## Установка проекта локально

В папке склонированного репозитория выполните:

```bash
docker-compose up -d --build
docker exec -it 12_06_emphasoft_web_1 python3 manage.py makemigrations
docker exec -it 12_06_emphasoft_web_1 python3 manage.py migrate
```

Далее загрузите в БД тестовые данные:
```bash
docker exec -it 12_06_emphasoft_web_1 python3 manage.py loaddata dump.json
```
## Пример .env файла

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
DB_HOST=db
DB_PORT=5432
SECRET_KEY=p&l%slhtyn^##a1)ilz@4zqj=rq&agdol^##zglmlkmklmewf16w5165^(*U)(&%3dkm9(vs
DEBUG=False
```

Файл должен находиться в корне проекта

## Документация API

доступна по адресу http://localhost/api/docs/redoc/ и http://localhost/api/docs/swagger/ при развёрнутом проекте

## Ключи поиска и сортировки комнат

- Цена больше 500 и сортировка по количеству спальных мест:
http://localhost/api/rooms/?price_min=200&order_by=capacity
- Количество спальных мест больше 3 и сортировка по цене по убыванию:
http://localhost/api/rooms/?capacity_min=3&order_by=-price
- Свободные номера с 2022-12-20 по 022-12-21:
http://localhost/api/rooms/?date_range_after=2022-12-20&date_range_before=2022-12-21


## Стек

Django, Django REST framework, Docker-compose, Nginx, PostgreSQL, Swagger


## Автор

Семён Егоров

[LinkedIn](https://www.linkedin.com/in/simonegorov/)  
[Email](simon.egorov.job@gmail.com)  
[Telegram](https://t.me/SamePersoon)  
