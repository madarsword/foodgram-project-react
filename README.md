# Данные для ревью:
> foodgramshpr.hopto.org
> aleksandrshpr@yandex.ru
> 36vdfbdfbdf16sdfsdfgsdf26

# Описание проекта
## «Фудграм» — сайт, на котором пользователи публикуют рецепты, добавляют чужие рецепты в избранное и подписываются на публикации других авторов. Пользователям сайта доступен сервис «Список покупок». Он позволяет скачивать список продуктов, которые нужно купить для приготовления выбранных блюд.

# Проект «Фудграм» доступен по ссылке:
> foodgramshpr.hopto.org

# Установка и запуск
### Клонируйте репозиторий:
> git clone git@github.com:madarsword/foodgram-project-react.git

### Установите Docker Compose на сервер:
> sudo apt update
> sudo apt install curl
> curl -fSL https://get.docker.com -o get-docker.sh
> sudo sh ./get-docker.sh
> sudo apt-get install docker-compose-plugin

### Скопируйте на сервер файлы проекта:
> docker-compose.yaml
> nginx.conf

### Добавьте секреты в GitHub Actions:
> DB_ENGINE=django.db.backends.postgresql
> DB_HOST=название БД (контейнера) 
> DB_NAME=имя БД
> DB_PORT=порт для подключения к БД
> DOCKER_PASSWORD=пароль от Docker Hub
> DOCKER_USERNAME=логин от Docker Hub
> HOST=IP-адрес сервера
> POSTGRES_PASSWORD=пароль для подключения к БД
> POSTGRES_USER=логин для подключения к БД
> SSH_KEY=SSH-ключ
> SSH_PASSPHRASE=фраза-пароль для SSH
> USER=логин на удалённом сервере

### Обновите данные репозитория:
```
git add .
```
```
git commit -m "Текст коммита"
```
```
git push
```

### Выполните на сервере последовательно команды:
```
sudo docker compose exec backend python manage.py migrate
```
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```
```
sudo docker compose exec backend python manage.py createsuperuser
```
```
sudo docker compose exec backend python manage.py import_ingredients --path data/ingredients.csv --model_name Ingredient --app_name recipes
```

## Запуск проекта локально
### Клонируйте репозиторий:
> git clone git@github.com:madarsword/foodgram-project-react.git

### Перейдите в директории:
> cd foodgram-project-react
> cd infra

### Запустите оркестрацию:
> docker compose up

### Выполните миграции:
> docker compose exec backend python manage.py migrate

### Создайте суперпользователя:
> docker compose exec backend python manage.py createsuperuser

### Загрузите статику:
> docker compose exec backend python manage.py collectstatic --no-input 

### Проверьте работу проекта по ссылке:
> http://localhost/

### Спецификация API:
> http://localhost/api/docs/

# Автор проекта
## Александр Шпара
