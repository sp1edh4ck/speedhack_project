# Generated by Django 3.2.18 on 2023-04-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_background',
            field=models.ImageField(blank=True, default='', null=True, upload_to='backgrounds/', verbose_name='Фон профиля'),
        ),
    ]
