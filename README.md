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
scp docker-compose.yaml sp1edh4ck@158.160.127.162:/home/sp1edh4ck/infra/

scp .env sp1edh4ck@158.160.127.162:/home/sp1edh4ck/infra/

scp default.conf sp1edh4ck@158.160.127.162:/home/sp1edh4ck/infra/nginx/
```

###### Запускаем команду которая совершает 3 действия:
- Обновляет список доступных пакетов.
- Устанавливает обновления для всех установленных пакетов на вашей системе.
- Устанавливает пакет curl на вашей системе.
```
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
```

###### Загружаем файл Docker Compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

###### Загружаем docker.io
```
sudo apt install docker.io
```

###### Данная команда позволит использовать команду docker-compose из любого места в системе.
```
sudo chmod +x /usr/local/bin/docker-compose
```

###### Данная команда будет автоматически запускать docker после перезагрузки системы.
```
sudo systemctl start docker.service && sudo systemctl enable docker.service
```

###### После этого деплоим проект, чтобы запустить github actions
###### Если деплой прошёл успешно, то переходим в папку ```cd infra``` и запускаем команду ```sudo docker-compose up -d --build``` на сервере

> Проект готов к работе!
