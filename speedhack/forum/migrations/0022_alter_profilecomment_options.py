# Generated by Django 3.2.18 on 2023-12-01 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0021_remove_profilecomment_unique_name_in_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profilecomment',
            options={'ordering': ('-created',), 'verbose_name': 'Комментарий на стене пользователя', 'verbose_name_plural': 'Комментарии на стене пользователя'},
        ),
    ]
