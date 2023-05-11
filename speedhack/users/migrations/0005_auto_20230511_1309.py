# Generated by Django 3.2.18 on 2023-05-11 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230427_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='privilege',
            field=models.TextField(choices=[('нет привилегий', 'нет привилегий'), ('продавец', 'продавец'), ('доверенный продавец', 'доверенный продавец'), ('партнёр', 'партнёр'), ('исскуственный интелект', 'исскуственный интелект')], default='нет привилегий', verbose_name='Привилегия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='rank',
            field=models.TextField(choices=[('пользователь', 'пользователь'), ('заблокирован', 'заблокирован'), ('местный', 'местный'), ('постоялец', 'постоялец'), ('эксперт', 'эксперт'), ('гуру', 'гуру'), ('куратор', 'куратор'), ('арбитр', 'арбитр'), ('администратор', 'администратор'), ('бот', 'бот'), ('гл. администратор', 'гл. администратор'), ('владелец', 'владелец')], default='пользователь', verbose_name='Ранг'),
        ),
    ]
