# Generated by Django 3.2.18 on 2023-05-11 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_customuser_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Симпатии'),
        ),
    ]
