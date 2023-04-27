# Generated by Django 3.2.18 on 2023-04-27 09:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Уникальный адрес')),
            ],
            options={
                'verbose_name': 'Платформа',
                'verbose_name_plural': 'Платформы',
            },
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55, verbose_name='Заголовок')),
                ('data', models.CharField(max_length=255, verbose_name='Данные от аккаунта')),
                ('price', models.IntegerField(validators=[django.core.validators.MaxValueValidator(150000)], verbose_name='Цена')),
                ('description', models.TextField(max_length=1000, verbose_name='Описание')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acc', to=settings.AUTH_USER_MODEL, verbose_name='Продавец')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='acc', to='market.accgroup', verbose_name='Платформа')),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
                'ordering': ('-pub_date',),
            },
        ),
    ]
