## Запуск

В этих примерах приложение будет доступно на порте 8080.

### Первый запуск

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 8080
```

### Последующие запуски

```
source .venv/bin/activate
python3 manage.py runserver 8080
```

## Способы обращения к API

Из требовавшихся по заданию:

1. `GET` по пути `/lesson/` с параметром `user_id`, соответствующим id интересующего пользователя.
2. `GET` по пути `/lesson/` с параметрами `user_id` и `product_id`, соответствующим id пользователя и продукта.
3. `GET` по пути `/stats/` без дополнительных параметров.

Также вне требований задания реализованы API для запросов GET:

|Путь|Описание|
|----|--------|
|users/|Список всех пользователей и купленных ими продуктов|
|products/owners/|Список всех продуктов и их владельцев|
|products/lessons/|Список всех продуктов и входящих в них уроков|

Все ответы приходят в формате JSON.
