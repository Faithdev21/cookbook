# CookBook Project

Документация (доступна после запуска проекта):

http://127.0.0.1/swagger/

http://127.0.0.1/redoc/

Проект упакован в контейнеры Docker для локального запуска.

Добавлены .csv файл вместе со специальной management-командой для заполнения БД.


### Технологии

Python 3.9, Django 3.2, DRF 3.14, Docker, PostgreSQL 13.0, Gunicorn 21.2, Nginx 1.21

### Запуск проекта локально

Склонируйте репозиторий:

```git clone git@github.com:Faithdev21/cookbook-project.git```

либо

```git clone https://github.com/Faithdev21/cookbook-project.git```

Добавьте файл с названием .env в backend/cookbook (туда же, где .env.example) и заполните его:

```
SECRET_KEY=django-insecure-r7=j=j2^+d-vx(rm%0wpa7b!r5t#wb#yeffoq2#co*^2(pg2oy
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,backend
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Из директории с docker-compose.yaml выполните:

```docker-compose up -d```

Для пересборки образа (в случае обновления содержимого проекта) дополните команду так:

```docker-compose up -d --build```

Примените миграции:

```docker-compose exec backend python manage.py migrate```

Создайте суперюзера:

```docker-compose exec backend python manage.py createsuperuser```

### Тестирование API

Для удобства тестирования можно выполнить команду загрузки тестовых данных в БД:

```docker-compose exec backend python manage.py import_csv```

### Основной функционал:

`http://127.0.0.1/api/add_product_to_recipe/`  

GET - Добавление к указанному рецепту указанный продукт с указанным весом. Параметры: recipe_id, product_id, weight.

Пример запроса:

`http://127.0.0.1/api/add_product_to_recipe/?recipe_id=1&product_id=61&weight=14`

Ответ: { "status": "Продукт добавлен} или {"status": "Вес продукта обновлен"} если продукт уже находился в рецепте.

---

`http://127.0.0.1:8000/api/cook_recipe/`

GET - Увеличивает на единицу количество приготовленных блюд для каждого продукта, входящего в указанный рецепт. Параметры: recipe_id.

Пример запроса:

`http://127.0.0.1:8000/api/cook_recipe/?recipe_id=5`

Ответ: {"status": "success"}

---

`http://127.0.0.1/api/show_recipes_without_product/`

GET - Вывод html страницы с id и названиями всех рецептов, в которых указанный продукт отсутствует, или присутствует в количестве меньше 10 грамм. Параметры: product_id

Пример запроса:

`http://127.0.0.1/api/show_recipes_without_product/?product_id=78`

Ответ:  
![image](https://github.com/Faithdev21/cookbook-project/assets/119350657/53cd13e0-136b-48ee-9298-6edcdc4f0ae9)  
Не вывелся еще один рецепт в который входил ингредиент с product_id=78  
Полный список рецептов:  
![image](https://github.com/Faithdev21/cookbook-project/assets/119350657/ab9b24ca-a36c-48e9-a027-bfee986d9cf9)

---

Документация API:

http://127.0.0.1/swagger/

http://127.0.0.1/redoc/

### Автор проекта

Егор Лоскутов

https://github.com/Faithdev21
