# Generated by Django 3.2.18 on 2023-04-08 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230408_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_sub',
            field=models.BooleanField(default=False, verbose_name='Доступ к фону профиля'),
        ),
    ]
