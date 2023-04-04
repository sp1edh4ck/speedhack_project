# speedhack_project

speedhack_project - это проект, который я делаю сам с абсолютного нуля.
---

### Как развернуть проект?

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
