# Generated by Django 3.2.18 on 2023-04-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20230412_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_online',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
