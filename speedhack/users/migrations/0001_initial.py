# Generated by Django 3.2.18 on 2023-05-19 20:54

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('likes', models.IntegerField(default=0, verbose_name='Симпатии')),
                ('balance', models.IntegerField(default=0, verbose_name='Баланс')),
                ('save_deposit', models.IntegerField(default=0, verbose_name='Страховой депозит')),
                ('gender', models.TextField(choices=[('Не выбрано', 'Не выбрано'), ('Мужской', 'Мужской'), ('Женский', 'Женский')], default='Не выбрано', verbose_name='Пол')),
                ('username_style', models.TextField(choices=[('gray-un', '.gray-un'), ('white-shadow-un', '.white-shadow-un'), ('grad-wb-un', '.grad-wb-un'), ('red-shadow-un', '.red-shadow-un'), ('grad-pwv-un', '.grad-pwv-un'), ('grad-bvr-un', '.grad-bvr-un'), ('grad-p-double-un', '.grad-p-double-un'), ('pink-shadow-un', '.pink-shadow-un'), ('purple-shadow-un', '.purple-shadow-un'), ('light-green-shadow-un', '.light-green-shadow-un'), ('grad-wp-un', '.grad-wp-un'), ('grad-wy-un', '.grad-wy-un'), ('grad-pp-un', '.grad-pp-un'), ('light-red-shadow-un', '.light-red-shadow-un'), ('blue-shadow-un', '.blue-shadow-un'), ('white-double-shadow-un', '.white-double-shadow-un'), ('blue-light-shadow-un', '.blue-light-shadow-un'), ('dark-green-shadow-un', '.dark-green-shadow-un'), ('blue-p-shadow-un', '.blue-p-shadow-un'), ('black-shadow-un', '.black-shadow-un'), ('red-orange-shadow-un', '.red-orange-shadow-un'), ('light-blue-double-shadow-un', '.light-blue-double-shadow-un'), ('aquamarine-shadow-un', '.aquamarine-shadow-un'), ('green-so-beautifull-un', '.green-so-beautifull-un')], default='gray-un', verbose_name='Стиль имени')),
                ('banner', models.TextField(choices=[('gray-role', '.gray-role'), ('green-yellow-role', '.green-yellow-role'), ('milk-pink-role', '.milk-pink-role'), ('purple-aquamarine-role', '.purple-aquamarine-role'), ('red-purple-role', '.red-purple-role'), ('yellow-green-role', '.yellow-green-role'), ('blue-pink-role', '.blue-pink-role')], default='gray-role', verbose_name='')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('occupation', models.CharField(default='', max_length=200, verbose_name='Род занятий')),
                ('interests', models.CharField(default='', max_length=200, verbose_name='Интересы')),
                ('description', models.CharField(default='', max_length=200, verbose_name='Описание')),
                ('rank', models.TextField(choices=[('пользователь', 'пользователь'), ('заблокирован', 'заблокирован'), ('дизайнер', 'дизайнер'), ('главный дизайнер', 'главный дизайнер'), ('куратор', 'куратор'), ('арбитр', 'арбитр'), ('главный арбитр', 'главный арбитр'), ('бот', 'бот'), ('администратор', 'администратор'), ('разработчик', 'разработчик'), ('гл. администратор', 'гл. администратор'), ('владелец', 'владелец')], default='пользователь', verbose_name='Должность')),
                ('save_rank', models.TextField(default='', verbose_name='Сохранённый ранг')),
                ('privilege', models.TextField(choices=[('нет привилегий', 'нет привилегий'), ('местный', 'местный'), ('постоялец', 'постоялец'), ('эксперт', 'эксперт'), ('гуру', 'гуру'), ('искусственный интелект', 'искусственный интелект')], default='нет привилегий', verbose_name='Ранг')),
                ('market_privilege', models.TextField(choices=[('нет привилегий', 'нет привилегий'), ('продавец', 'продавец'), ('доверенный продавец', 'доверенный продавец'), ('партнёр', 'партнёр')], default='нет привилегий', verbose_name='Привилегия на маркете')),
                ('buy_privilege', models.TextField(choices=[('нет привилегий', 'нет привилегий'), ('легенда', 'легенда'), ('суприм', 'суприм'), ('уник', 'уник')], default='нет привилегий', verbose_name='Платные привилегии')),
                ('time_buy_privilege', models.DateField(default=datetime.datetime(2023, 5, 19, 20, 54, 53, 673185, tzinfo=utc), verbose_name='Дата покупки привилегии')),
                ('time_buy_profile_sub', models.DateField(default=datetime.datetime(2023, 5, 19, 20, 54, 53, 673185, tzinfo=utc), verbose_name='Дата покупки фона профиля')),
                ('time_buy_market_privilege', models.DateField(default=datetime.datetime(2023, 5, 19, 20, 54, 53, 673185, tzinfo=utc), verbose_name='Дата покупки доступа к маркету')),
                ('profile_sub', models.BooleanField(default=False, verbose_name='Доступ к фону профиля')),
                ('messages', models.IntegerField(default=0, verbose_name='Сообщения')),
                ('tg_link', models.CharField(blank=True, default='', max_length=70, verbose_name='Ссылка на телеграм')),
                ('subscriber', models.IntegerField(default=0, verbose_name='Подписчики')),
                ('avatar', models.ImageField(blank=True, default='default.png', null=True, upload_to='avatars/', verbose_name='Аватар')),
                ('profile_background', models.ImageField(blank=True, null=True, upload_to='backgrounds/', verbose_name='Фон профиля')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
