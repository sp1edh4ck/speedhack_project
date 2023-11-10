### Развёртка проекта локально

###### Загружаем проект себе на пк
```
git clone https://github.com/sp11dh4ck/speedhack_project
```

###### Ставим виртуальное окружение и устанавливаем нужные библиотеки
```
cd speedhack

python -m venv venv

source venv/Scripts/activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

pip install djoser

pip install django-filter
```

###### Выполняем миграции
```
cd speedhack

python manage.py runserver (для создания базы данных)

После останавливаем сервер и создаём миграции отдельно для всех приложений, чтобы избежать ошибок

python manage.py makemigrations (users, forum)

python manage.py migrate
```

> Проект готов к работе!

---

### Развёртка проекта на сервере (yandex cloud)

###### Заходим на сервер
```
ssh -o ServerAliveInterval=30 sp1edh4ck@158.160.127.162
```

###### Создаём нужные папки
```
cd ~

mkdir infra

cd infra

mkdir nginx
```

###### Выходим с сервера и загружаем файлы (docker-copmose.yml, .env, default.conf)
```
scp docker-composa.yml sp1edh4ck@158.160.127.162:/home/sp1edh4ck/infra/

scp .env sp1edh4ck@158.160.127.162:/home/sp1edh4ck/infra/

scp default.conf sp1edh4ck@158.160.127.162:/home/sp1edh4ck/infra/nginx/
```

###### После этого деплоим проект, чтобы запустить github actions
###### Если деплой прошёл успешно, то надо запустить команду ```sudo docker-compose up -d --build``` на сервере

> Проект готов к работе!
