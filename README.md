```Foodgram - Продуктовый помощник. Сервис позволяет публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин - скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.```
```
https://boaruzhan-foodgram.sytes.net
```
```Клонируйте репозиторий и перейдите в него в командной строке:```
```
git clone https://github.com/boaruzhanchik/foodgram-project-react.git
cd backend
```
```Создайте и активируйте виртуальное окружение, обновите pip:```
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
```

```Как развернуть проект на сервере:```
```Установите соединение с сервером:```
```
ssh -i <путь до ссш>username@server_address
```
```Обновите индекс пакетов APT:```
```
sudo apt update
```
```и обновите установленные в системе пакеты и установите обновления безопасности:```
```
sudo apt upgrade -y
```
```
Создайте папку `nginx`:
```
```
mkdir nginx
```
```
Отредактируйте файл `nginx/default.conf` и в строке `server_name` впишите IP виртуальной машины (сервера).  
Скопируйте подготовленные файлы `docker-compose.yml` и `nginx/default.conf` из вашего проекта на сервер:
```
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
```Установите Docker и Docker-compose:```
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
```
Проверьте корректность установки Docker-compose:
```
```
sudo  docker-compose --version
```
На сервере создайте файл .env 
```
touch .env
```
```
и заполните переменные окружения
```
```
nano .env
```
```
или создайте этот файл локально и скопируйте файл по аналогии с предыдущим шагом:
```
```
SECRET_KEY=<SECRET_KEY>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres-container
POSTGRES_USER=foodgrampost
POSTGRES_PASSWORD=foodgrampost
DB_HOST=db
DB_PORT=5432
```

### После успешного деплоя:
На сервере соберите docker-compose:
```
sudo docker-compose up -d --build
```
Соберите статические файлы (статику):
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Примените миграции:
```
(опционально) docker-compose exec backend python manage.py makemigrations
```
```
docker-compose exec backend python manage.py migrate --noinput
```
Создайте суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
При необходимости наполните базу тестовыми данными из backend/data/:
```
docker-compose exec backend python manage.py import_data
```

#### Операции с пользователями:
- ```api/users/``` - получение информации о пользователе и регистрация новых пользователей. (GET, POST).
- ```api/users/{id}/``` - Получение информации о пользователе. (GET).
- ```api/users/me/``` - получение и изменение данных своей учётной записи. Доступна любым авторизованными пользователям (GET).
- ```api/users/set_password/``` - изменение собственного пароля (PATCH).
- ```api/users/{id}/subscribe/``` - Подписаться на пользователя с соответствующим id или отписаться от него. (GET, DELETE).
- ```api/users/subscribe/subscriptions/``` - Просмотр пользователей на которых подписан текущий пользователь. (GET).

#### Аутентификация и создание новых пользователей 👇:
- ```api/auth/token/login/``` - Получение токена (POST).
- ```api/auth/token/logout/``` - Удаление токена (POST).

#### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос для регистрации нового пользователя с параметрами
***email username first_name last_name password***
на эндпойнт ```/api/users/```
2. Пользователь отправляет POST-запрос со своими регистрационными данными ***email password*** на эндпоинт ```/api/token/login/``` , в ответе на запрос ему приходит auth-token. Примечание: При взаимодействии с фронтэндом приложения операция два происходит под капотом при переходе по эндпоинту ```/api/token/login/```.
