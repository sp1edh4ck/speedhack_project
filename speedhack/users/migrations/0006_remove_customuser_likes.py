# Generated by Django 3.2.18 on 2023-05-11 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230511_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='likes',
        ),
    ]
